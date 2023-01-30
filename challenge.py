import time
from distribute_challenge import compute_this

@compute_this
def func(x):
	time.sleep(x)
	return x*x

out = func(3).run()
assert out == 9
# print(out)