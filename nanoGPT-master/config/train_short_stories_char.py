# config/train_short_stories.py

out_dir = 'out-short-stories'
eval_interval = 500
eval_iters = 200
log_interval = 10
always_save_checkpoint = True

wandb_log = False # override via command line if you like
wandb_project = 'short-stories'
wandb_run_name = 'mini-gpt'

dataset = 'short_stories'
batch_size = 4
block_size = 128 # context of up to 128 previous characters

# model
n_layer = 6
n_head = 6
n_embd = 384
dropout = 0.2

# adamw optimizer
learning_rate = 6e-4
max_iters = 20000
lr_decay_iters = 20000
min_lr = 6e-5
beta2 = 0.99

warmup_iters = 100
