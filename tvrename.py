import pathlib

from pytvdbapi import api


def rename():
    cwd = pathlib.Path.cwd()
    show_name = cwd.parent.name
    season_num = int(cwd.name.rsplit()[-1])

    episode_names = get_episode_names(show_name, season_num)
    files = sorted(cwd.iterdir())

    assert len(episode_names) == len(files)

    for file_, episode_name in zip(files, episode_names):
        new_name = file_.with_name(episode_name).with_suffix(file_.suffix)
        print(file_.name, '->', new_name.name)
    print()

    if input("Continue? (y/n) ").lower() == 'y':
        for file_, episode_name in zip(files, episode_names):
            new_name = file_.with_name(episode_name).with_suffix(file_.suffix)
            if file_ != new_name:
                file_.rename(new_name)


def get_episode_names(show_name, season_num):
    db = api.TVDB("B43FF87DE395DF56")
    show = db.search(show_name, 'en')[0]
    season = show[season_num]
    return [format_name(i + 1, e.EpisodeName) for i, e in enumerate(season)]


def format_name(episode_num, name):
    return "{:02d} - {}".format(episode_num, name)


if __name__ == "__main__":
    rename()
