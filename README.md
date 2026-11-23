[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/ixciamakima/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/ixciamakima/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# The World in One Day — Monday, 23 November 2026

One broadsheet front page that sums up Monday 23 November 2026's world
news in a single 1024x1024 image: 15 stories from 7 regions, a numbered
world map, a markets strip (close Fri 20 Nov), and a day-in-numbers cell.

## Stories (every fact verified against two independent sources)

| # | Story | Sources |
|---|-------|---------|
| 1 | COP31 collapses in Antalya: no deal, fossil fuels unnamed; longest COP ever, first breakdown since COP15 (2009) | CNN, Le Monde, Reuters, Business Day |
| 2 | Iran strikes Bahrain (Sat 21 Nov): 2 wounded, 1 critical; Saudi Arabia condemns "criminal" attacks; Houthi fire reaches Riyadh | AFP, Xinhua, AP |
| 3 | Russian drone collapses a five-storey block in Dymer, Kyiv region: 14 unaccounted for, 9 evacuated, 1 body found | Reuters, France 24, IBTimes |
| 4 | "El Chapo Isidro" captured in Guasave, Sinaloa; 11 killed (7 gunmen, 4 soldiers); FBI Top 10 fugitive | CNN, AP |
| 5 | South Korea education minister Choi Kyo-jin resigns over CSAT AI-cheating chaos; 111 cases caught | Korea JoongAng Daily, AFP |
| 6 | Candy factory fire in Cikande, Java: 7 body bags recovered, ~50 missing (police) | Reuters, AP |
| 7 | UN talks on lethal autonomous weapons, Geneva: 2 more years of talks, no binding rules; accord aimed at 2028 | NPR/AP |
| 8 | Nepal PM Balendra Shah holds talks with PM Modi in New Delhi (Mon 23 Nov) | IANS, ANI |
| 9 | India 720/9 declared at Wellington — highest Test total in New Zealand; lead 352; NZ 119/2 | Cricinfo, Cricbuzz |
| 10 | Russian cargo ship Sparta II hit by drones in the Gulf of Finland; 16 crew evacuated; Finland says Ukraine likely behind it | Reuters, CNN |
| 11 | Democrats clinch 258 US House seats — biggest majority since 1992; +44 seats | Reuters, AP |
| 12 | Rebels kill at least 15 civilians in a cattle-camp raid, Tonj East, South Sudan | AFP |
| 13 | UK and EU seal Brexit reset deal: food checks to end, 100,000 youth visas a year each way | Le Monde, Irish Times, The Times |
| 14 | Jair Bolsonaro, 71, stable in intensive care in Brasilia with a bowel obstruction | The Times, Reuters |
| — | Markets, close Fri 20 Nov: Brent $92.57 (-3.4% wk); S&P 500 6,910 (-3.7%); Nasdaq 22,618 (-5.3%); Dow 48,147 (-1.9%); OPEC+ meets 29 Nov | PTI/EnergyNow, AP, Investopedia |

Event dates are labelled honestly on every story: most of the day's news
broke on Sunday 22 November and is summed up here on Monday 23 November,
the day this front page is dated. The Nepal–Modi talks take place on
Monday 23 November itself.

## How to render

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Writes `entry.png` (1024x1024 PNG, under 1 MiB). Deterministic: no
network, no clock, no randomness — two runs produce byte-identical output
(verified: same SHA-256).

## Files

- `main.py` — entrypoint; renders and writes `/output/entry.png`
- `render.py` — all drawing: masthead, three lead illustrations, world map,
  markets strip, story grid (Pillow, Noto fonts)
- `entry.png` — the rendered front page
- `LICENSE` — MIT

## License

MIT — see LICENSE.
