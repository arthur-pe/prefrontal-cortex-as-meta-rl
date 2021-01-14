from meta_rl.models import PrefrontalLSTM
from meta_rl.training import train
from meta_rl.tasks import TaskOne, TwoStep, HumanTwoStep
import torch
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
from scipy.interpolate import make_interp_spline, BSpline
import gym

model = PrefrontalLSTM(2, 2, hidden_size=192)
model.train()
optimizer = torch.optim.RMSprop(model.parameters(), lr=0.0007)
env = HumanTwoStep()
loss = []
rewards = []
t_range = tqdm(range(30000))
for i in t_range:
    l, r, a = train(env, model, optimizer, discount_factor=0.90)
    t_range.set_description("Current loss: {:10.2f}".format(l))
    loss.append(l)
    rewards.append(sum(r) / len(r))

torch.save(model.state_dict(), 'human_task_two_30k_192.pt')
fig, axs = plt.subplots(2)

def smooth(X):
    X = np.array(X)
    T = np.arange(len(X))
    return np.poly1d(np.polyfit(T, X, 5))(T)

axs[0].plot(smooth(loss))
axs[0].plot(loss, alpha=0.25)
axs[0].set_title("Loss")

axs[1].plot(smooth(rewards))
axs[1].plot(rewards, alpha=0.25)
axs[1].set_title("Rewards")
plt.savefig("human_task_30k_192.png")
