import numpy as np
import tensorflow as tf

import gen2
from game_board import GameBoard

# input_units = 4**3 + 4*6
input_units = 4*3
hidden_units = 8
output_units = 4

learning_rate = 1e-3
discount_factor = 0


input_board = tf.placeholder(tf.float32, shape=[None, input_units])

W1 = tf.Variable(tf.truncated_normal([input_units, hidden_units], stddev=0.1))
b1 = tf.Variable(tf.constant(0.1, shape=[hidden_units]))

h1 = tf.nn.relu(tf.matmul(input_board, W1) + b1)

W2 = tf.Variable(tf.truncated_normal([hidden_units, output_units], stddev=0.1))
b2 = tf.Variable(tf.constant(0.1, shape=[output_units]))

output_raw = tf.matmul(h1, W2) + b2

output_op = tf.nn.softmax(tf.nn.relu(output_raw))

tvars = tf.trainable_variables()


# update cost function to multiply actions vector by output so only the relevant output is there
actions_holder = tf.placeholder(tf.float32, [None, output_units])
rewards_holder = tf.placeholder(tf.float32, [None, 1])

loglik = tf.log(actions_holder * (actions_holder - output_op) + (1 - actions_holder) * (actions_holder + output_op))
loss = -tf.reduce_mean(loglik * rewards_holder)

cross_entropy = rewards_holder * \
                tf.reduce_mean(-tf.reduce_sum(actions_holder * tf.log(output_op), reduction_indices=[1]))

grads = tf.gradients(cross_entropy, tvars)


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
            return action

num_total = 200000
batch_size = 2

num_batches = num_total // batch_size

saver = tf.train.Saver()

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    for current_batch in range(num_batches):
        with open('stop.txt') as stop_file:
            line = stop_file.readline()
            if line == 'y':
                break
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

                output = sess.run(output_op, feed_dict={
                    input_board: observation
                })

                # it might be a good idea to make this probabilistic, not deterministic
                action = get_action(output)

                action_vec = np.zeros(output_units)
                action_vec[action] = 1

                observation, reward, done, _ = board.step(action, display=False)

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

        if current_batch % ((50 // batch_size) or 1) == 0:
            print("Batch {}".format(current_batch))
            print("Average reward: {}".format(batch_reward / batch_size))
            print("Average steps: {}".format(batch_steps / batch_size))

    saver.save(sess, './model2')
