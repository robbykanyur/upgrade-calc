# upgrade-calc

Automatically calculates upgrade points for racers on crossresults.com

---

## sample env file

```
DB_PATH=./db/main.db
```

## to-do list

* Fine-tune category matching (e.g. a combined field like "Men Cat 3 - 40+ 50+" will get ignored even if the racer age is under 40)
  * See fields at the [2023 Major Taylor Cross Cup](https://www.crossresults.com/race/11848) for examples of this