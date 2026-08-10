# Contributing

Every change must:

1. remain inside one bounded work package;
2. add or update a failing semantic test before behavior;
3. preserve the frozen native lane or explicitly update its evidence;
4. pass contract and applicable Nix/native verification;
5. document evidence state and limitations; and
6. receive review from someone other than the author before release.

Run:

```bash
python3 -m unittest discover -s tests -v
```
