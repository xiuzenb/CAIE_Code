from .history import HOME_PATH
from .animation import new_animation
import os
import git

VERSION = ''

super_fast = False

with open(os.path.join(HOME_PATH, 'VERSION'), 'r') as f:
    VERSION = f.read().strip()


def check_update(repo: git.Repo, remote: git.Remote):
    remote.fetch()
    local_branch = repo.active_branch
    from .global_var import config
    config_branch = config.get_config('branch') if not config.get_config('dev') else 'dev'
    remote_branch = repo.remotes.origin.refs[config_branch]
    # 获取本地和远程提交的时间戳
    local_commit_time = local_branch.commit.committed_datetime
    remote_commit_time = remote_branch.commit.committed_datetime
    # 比较时间戳
    if local_commit_time < remote_commit_time:
        return True
    elif local_commit_time > remote_commit_time:
        print(f"Good! Good! You are faster than \033[1m{get_current_branch()}\033[0m branch!")
        print("At", *get_commit_hash_msg())
        global super_fast
        super_fast = True
        return False
    else:
        return False

def _update(remote, repo):
    try:
        from .global_var import config
        branch = config.get_config('branch') if not config.get_config('dev') else 'dev'
        repo.git.reset('--hard', f'origin/{branch}')
        repo.git.checkout(branch)
        remote.pull()
        print('\033[1mUpdate Successful\033[0m')
    except:
        print('\033[31;1mFailed to Update\033[0m')

def get_current_branch():
    repo = git.Repo(HOME_PATH)
    current_branch = repo.git.rev_parse("--abbrev-ref", "HEAD")
    return current_branch

def get_commit_hash_msg():
    repo = git.Repo(HOME_PATH)
    latest_commit_hash = repo.head.reference.commit.hexsha[:7]
    latest_commit_message = repo.head.reference.commit.message.strip()
    return latest_commit_hash, latest_commit_message

def update():
    from .global_var import config
    git_remote = config.get_config('remote')
    repo = git.Repo(HOME_PATH)
    remote = repo.remote()
    if config.get_config('dev'):
        print('In a developer mod, your remote will not be changed by config and branch will be locked in dev.')
        print('You can close the developer mod by using `cpc -c dev false`.')
    else:
        remote.set_url(git_remote)
    # 获取当前commit记录
    latest_commit_hash, latest_commit_message = get_commit_hash_msg()

    if new_animation('Checking Update', 3, check_update, failed_msg='Failed to Check Update', repo=repo, remote=remote):
        # 更新后再次获取新的commit记录
        _update(remote, repo)
        latest_commit_hash, latest_commit_message = get_commit_hash_msg()
        # 询问是否更新
        u = input(f'There is a new \033[1m{get_current_branch()}\033[0m version of the program\n{latest_commit_hash}: {latest_commit_message}\nDo you want to update it? [Y/n] ').strip().lower()
        if u == '' or u == 'y':
            if new_animation('Updating', 3, _update, failed_msg='Failed to Update', remote=remote, repo=repo):
                print('\033[1mUpdate Successful\033[0m')
        else:
            print('Stop Updating')
    else:
        if not super_fast:
            # 更新后再次获取新的commit记录
            latest_commit_hash, latest_commit_message = get_commit_hash_msg()
            print(f'Good! You are using the latest \033[1m{get_current_branch()}\033[0m version!\nAt {latest_commit_hash}: {latest_commit_message}')
