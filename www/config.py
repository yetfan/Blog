# -*- coding: utf-8 -*-
# 综合本地和服务器设置
import config_default


class Dict(dict):
	"""
	Simple dict but support access as "dict.x = y" style.
	"""

	def __init__(self, names=(), values=(), **kw):
		super(Dict, self).__init__(**kw)
		for k, v in zip(names, values):
			self[k] = v

	def __getattr__(self, key):
		try:
			return self[key]
		except KeyError:
			raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

	def __setattr__(self, key, value):
		self[key] = value


def merge(default, override):
	r = {}
	for k, v in default.items():  # 遍历默认
		if k in override:  # 如果存在于新设置
			if isinstance(v, dict):  # 新设置为字典 继续合并字典内部
				r[k] = merge(v, override[k])
			else:
				r[k] = override[k]  # 覆盖，使用新设置
		else:
			r[k] = v  # 如果不存在于新设置，使用默认
	return r


def toDict(config):
	# 转化为字典类实例
	d = Dict()
	for k, v in config.items():
		# 字典内部有字典形式继续转 例如{'session': {'secret': 'AwEsOmE'}, 'db': {'port': 3306, 'user': 'blog'}}
		d[k] = toDict(v) if isinstance(v, dict) else v
	return d


configs = config_default.configs

try:
	import config_override
	configs = merge(configs, config_override.configs)
except ImportWarning:
	pass

configs = toDict(configs)
