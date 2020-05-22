s, t = [input() for _ in range(2)]
print(sum(1 for i in range(len(s)) if s.startswith(t, i)))