#!/usr/bin/env python3

# imports
# -----------------------------
import sys
import argparse

# parse arguments
# -----------------------------
parser = argparse.ArgumentParser(
  description="Generate a Goodstein sequence started from an initial value")
parser.add_argument("initial_value", help="the initial value of the Goodstein sequence", type=int)
parser.add_argument("sequence_length", help="the number of terms to compute", type=int)
args = parser.parse_args()

# source code
# -----------------------------
def expand_in_base(n, b):

  # write n in b-ary
  raw_string = ""
  raw_list = []

  i = 0
  while n > 0:
    raw_string = str(n % b) + raw_string
    raw_list.insert(0, str(n % b))
    n //= b
    i += 1

  # make readable
  n_digits = len(raw_list)
  readable_list = n_digits * [None]
  for k in range(n_digits):

    coefficient = raw_list[k]
    power = str(n_digits - k - 1)
    base = str(b)

    if coefficient == "0":
      readable_list[k] = ""

    elif coefficient == "1":
      if power == "0":
        readable_list[k] = "1"
      elif power == "1":
        readable_list[k] = base
      else:
        readable_list[k] = base + "^" + power

    else:
      if power == "0":
        readable_list[k] = coefficient
      elif power == "1":
        readable_list[k] = coefficient + "*" + base
      else:
        readable_list[k] = coefficient + "*" + base + "^" + power

  readable_string = "+".join([s for s in readable_list if not s ==""])

  return readable_string


def max_digit(string):

  return(max([int(x) for x in string if x.isdigit()]))


def cantor_in_base(n, b):

  cantor_expansion = expand_in_base(n, b)
  m = max_digit(cantor_expansion)

  while m > b:
    max_digit_replacement = "(" + expand_in_base(m, b) + ")"
    cantor_expansion = cantor_expansion.replace(str(m), max_digit_replacement)
    m = max_digit(cantor_expansion)

  return(cantor_expansion)


def goodstein_iter(n, b):

  cantor_expansion = cantor_in_base(n, b)
  substituted_base = cantor_expansion.replace(str(b), str(b+1))
  fix_exponent_symbol = substituted_base.replace("^", "**")
  eval_and_reduce = eval(fix_exponent_symbol) - 1

  return(eval_and_reduce)


def goodstein(n, seq_len):

  value = n

  for k in range(0, seq_len):

    b = k + 2

    print("")
    print(value)
    print(cantor_in_base(value, b))

    value = goodstein_iter(value, b)

  return


# run
# -----------------------------
initial_value = args.initial_value
sequence_length = args.sequence_length
goodstein(initial_value, sequence_length)
