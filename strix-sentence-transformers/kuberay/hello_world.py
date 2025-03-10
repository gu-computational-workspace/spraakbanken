#!/usr/bin/python
import ray
import time

def get_string_to_display():
  return "bla"

# @ray.remote
def hello_world():
  rtn_str = get_string_to_display()
  return rtn_str

#ray.init(address="ray://127.0.0.1:8265/")

ray.init()
#print(ray.get(hello_world.remote()))
print(hello_world())
