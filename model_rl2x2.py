import numpy as np
import tensorflow as tf

import gen2
from game_board import GameBoard

input_units = 4**3 + 4*6
hidden_units = (4**3) // 2
# outputs are row col num commit, only does one at a time
output_units = 4*3

learning_rate = 1e-4
discount_factor = 0.8


input_board = tf.placeholder(tf.float32, shape=[None, input_units])

W1 = tf.Variable(tf.truncated_normal([input_units, hidden_units], stddev=0.1))
b1 = tf.Variable(tf.constant(0.1, shape=[hidden_units]))

h1 = tf.nn.relu(tf.matmul(input_board, W1) + b1)

W2 = tf.Variable(tf.truncated_normal([hidden_units, output_units], stddev=0.1))
b2 = tf.Variable(tf.constant(0.1, shape=[output_units]))

output_raw = tf.matmul(h1, W2) + b2

eval_output = tf.nn.softmax(output_raw)

tvars = tf.trainable_variables()


# update cost function to multiply actions vector by output so only the relevant output is there
actions_holder = tf.placeholder(tf.float32, [None, output_units])
rewards_holder = tf.placeholder(tf.float32, [None, 1])
loglik = tf.log(actions_holder*(actions_holder - eval_output) + (1 - actions_holder)*(actions_holder - eval_output))
loss = -tf.reduce_mean(loglik * rewards_holder)
grads = tf.gradients(loss, tvars)


adam = tf.train.AdamOptimizer(learning_rate)
W1_grad = tf.placeholder(tf.float32)
b1_grad = tf.placeholder(tf.float32)
W2_grad = tf.placeholder(tf.float32)
b2_grad = tf.placeholder(tf.float32)
all_grads = [W1_grad, b1_grad, W2_grad, b2_grad]
update = adam.apply_gradients(zip(all_grads, tvars))


def get_action(action_vec):
    action_vec = action_vec.reshape([output_units])
    num = np.random.rand()
    action_sum = 0.0
    for action, probability in enumerate(action_vec):
        action_sum += probability
        if num < action_sum:
            return action  # action


def apply_discount(rewards):
    discounted_rewards = np.zeros_like(rewards)
    running_reward = 0
    for i in reversed(range(rewards.size)):
        running_reward = running_reward * discount_factor + reward
        discounted_rewards[i] = running_reward
    return discounted_rewards

num_batches = 1000
batch_size = 50

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    for current_batch in range(num_batches):
        puzzles, solutions = gen2.get_vector_batch(batch_size)

        batch_reward = 0
        batch_steps = 0

        batch_grads = sess.run(tvars)
        for i, grad in enumerate(batch_grads):
            batch_grads[i] = grad * 0

        for step_num in range(batch_size):
            board = GameBoard(puzzles[step_num], solutions[step_num])
            done = False
            step_num = 0

            actions = []
            observations = []
            rewards = []

            observation = board.get_vec()

            while not done:

                output = sess.run(eval_output, feed_dict={
                    input_board: observation
                })

                # it might be a good idea to make this probabilistic, not deterministic
                action = get_action(output)

                action_vec = np.zeros(output_units)
                action_vec[action] = 1

                observation, reward, done, _ = board.step(action)

                batch_reward += reward

                # add observation and reward to list
                actions.append(action_vec)
                observations.append(observation)
                rewards.append(reward)

                step_num += 1
                batch_steps += 1

                if step_num > 40:
                    break

            observations = np.vstack(observations)
            actions = np.vstack(actions)
            rewards = np.vstack(rewards)

            rewards = apply_discount(rewards)
            rewards -= np.mean(rewards)
            if np.std(rewards) != 0:  # Don't want to divide by zero!
                rewards /= np.std(rewards)

            episode_grads = sess.run(grads, feed_dict={
                input_board: observations,
                actions_holder: actions,
                rewards_holder: rewards
            })

            # setting an array element with a sequence
            for grad_index, grad in enumerate(episode_grads):
                batch_grads[grad_index] += grad

        sess.run(update, feed_dict={
            W1_grad: batch_grads[0],
            b1_grad: batch_grads[1],
            W2_grad: batch_grads[2],
            b2_grad: batch_grads[3]
        })

        print("Batch {}".format(current_batch))
        print("Average reward: {}".format(batch_reward / batch_size))
        print("Average steps: {}".format(batch_steps / batch_size))

