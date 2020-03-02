# goodstein-calculator

Python script for calculating Goodstein sequences

## Dependencies
- Python 3

## Usage
```python3 goodstein_calculator.py INITIAL_VALUE SEQUENCE_LENGTH --colorize```

## Notes
- For initial values of 3 or less, the Goodstein sequence rapidly converges to zero and terminates.
- For initial values of 4 or above, you will never see the sequence hit zero in any simulation.
- However it can be proven (as on my [blog](https://wgunderwood.github.io/2020/01/08/goodstein-sequences.html)) that all Goodstein sequences eventually terminate at zero.
