#!/usr/bin/env python3

# imports
# -----------------------------
import re
import argparse
import sys

sys.set_int_max_str_digits(1000000000)

# parse command line arguments
# -----------------------------
parser = argparse.ArgumentParser(
  description="Generate a Goodstein sequence started from an initial value")
parser.add_argument("initial_value", help="the initial value of the Goodstein sequence", type=int)
parser.add_argument("sequence_length", help="the number of terms to compute", type=int)
parser.add_argument("--colorize", help="colorize terminal output",
                    action="store_true")
args = parser.parse_args()

# source code
# -----------------------------
def expand_in_base(n, b):

  '''expand n in base b, and return a human-readable string'''

  if not type(n) == int:
    raise(TypeError("n must be an integer"))

  if not n >= 0:
    raise(ValueError("n must be non-negative"))

  if not type(b) == int:
    raise(TypeError("b must be an integer"))

  if not b >= 2:
    raise(ValueError("b must be at least 2"))

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

  '''return the largest single digit present in a string'''

  if not type(string) == str:
    raise(TypeError("string must be a string"))

  regex = [x for x in re.split("[^0-9]", string) if x != ""]

  return max(map(int, regex))


def cantor_in_base(n, b):

  '''write n in cantor normal form to base b, and return a human-readable string'''

  if not type(n) == int:
    raise(TypeError("n must be an integer"))

  if not n >= 0:
    raise(ValueError("n must be non-negative"))

  if not type(b) == int:
    raise(TypeError("b must be an integer"))

  if not b >= 2:
    raise(ValueError("b must be at least 2"))

  if n == 0:
    return "0"

  cantor_expansion = expand_in_base(n, b)
  m = max_digit(cantor_expansion)

  while m > b:
    max_digit_replacement = "(" + expand_in_base(m, b) + ")"
    cantor_expansion = cantor_expansion.replace(str(m), max_digit_replacement)
    m = max_digit(cantor_expansion)

  return(cantor_expansion)


def goodstein_iter(n, b):

  '''perform a single Goodstein iteration with base b, and return an integer'''

  if not type(n) == int:
    raise(TypeError("n must be an integer"))

  if not n >= 0:
    raise(ValueError("n must be non-negative"))

  if not type(b) == int:
    raise(TypeError("b must be an integer"))

  if not b >= 2:
    raise(ValueError("b must be at least 2"))

  if n == 0:
    return 0

  cantor_expansion = cantor_in_base(n, b)
  substituted_base = cantor_expansion.replace(str(b), str(b+1))
  fix_exponent_symbol = substituted_base.replace("^", "**")
  eval_and_reduce = eval(fix_exponent_symbol) - 1

  return(eval_and_reduce)


def goodstein(n, seq_len, colorize=False):

  '''generate a Goodstein sequence with given initial value and length'''

  if not type(n) == int:
    raise(TypeError("n must be an integer"))

  if not n >= 0:
    raise(ValueError("n must be non-negative"))

  if not type(seq_len) == int:
    raise(TypeError("seq_len must be an integer"))

  if not seq_len >= 1:
    raise(ValueError("seq_len must be at least one"))

  value = n

  for k in range(0, seq_len):

    b = k + 2

    print("")
    print("Term number: " + str(k+1))
    print("Sequence value: ", end="")

    if colorize:
      print('\033[32m' + str(value) + '\033[0m')
    else:
      print(value)

    print("Cantor normal form: ", end="")
    if colorize:
      print('\033[35m' + cantor_in_base(value, b) + '\033[0m')
    else:
      print(cantor_in_base(value, b))

    if value == 0:
      return

    if not k == seq_len - 1:
      value = goodstein_iter(value, b)

  return


# run
# -----------------------------
initial_value = args.initial_value
sequence_length = args.sequence_length
colorize = args.colorize
goodstein(initial_value, sequence_length, colorize)
