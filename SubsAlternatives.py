
def solve(s):
   stack = []
   op = {
      "|": lambda x, y: x or y,
      "&": lambda x, y: x and y,
   }
   for v in s.split():
      if v[0] == "(":
         stack.append(v[v.count("(") :] == "True")
      elif v.count(")") > 0:
         ct = v.count(")")
         stack.append(v[:-ct] == "True")
         for _ in range(ct):
            right = stack.pop()
            o = stack.pop()
            left = stack.pop()
            stack.append(o(left, right))
      elif v in ["True", "False"]:
         stack.append(v == "True")
      else:
         stack.append(op[v])

   if len(stack) > 1:
      for i in range(0, len(stack) - 1, 2):
         stack[i + 2] = stack[i + 1](stack[i], stack[i + 2])
      return stack[-1]

   return stack[0]


s = "True & (False | True)"
print(solve(s))


# or() / and() simply use join() to join the 3 given value by ply