[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/AARenor/makefun-news-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard)
[![reward](https://make.fun/badge/news-image-20261123/AARenor/makefun-news-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123)

A 1024x1024 news card that sums up 23 November 2026 in six panels: a burning
cargo ship off Finland, Brent crude at $124.77, Myanmar rejecting an ASEAN
ruling, Nepal asking for flood aid, a chip-smuggling network in Singapore, and
houses burned in unrest at Narail, Bangladesh. `draw.py` is the Pillow renderer;
`main.py` copies the finished PNG, `entry.png`, that sits next to it, so a run
needs no network and no image library. `python3 main.py` writes
`/output/entry.png`, and `MAKEFUN_OUTPUT_DIR=/tmp/newsout python3 main.py` writes
it to another directory.
