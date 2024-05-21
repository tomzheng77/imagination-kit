import fnmatch
import hashlib
import os
import json
import csv
import shutil
import re
import time
import mimetypes
from dataclasses import dataclass, asdict
from typing import Type, Optional, List

from imk.imk_collections import ImkList


class ImkIo:

    def __init__(self, s100):
        self.s100 = s100

    def __call__(self, *args, **kwargs) -> 'ImkIoInDir':
        return ImkIoInDir(self.s100, self.s(*args))

    def sfx(self, path):
        """returns the suffix of a file"""
        return os.path.splitext(self.s(path))[1]

    def rfx(self, path, new_suffix):
        """changes the suffix of a file"""
        path = self.s(path)
        return os.path.splitext(path)[0] + new_suffix

    def rp(self, path, old, new):
        """replaces one string with another in a file"""
        path = self.s(path)
        with open(path, 'r') as f:
            s = f.read()
        s = s.replace(old, new)
        with open(path, 'w') as f:
            f.write(s)

    def s(self, *args) -> Optional[str]:
        if len(args) == 1 and isinstance(args[0], str):
            return os.path.expanduser(args[0])

        path = self.s100.py.coll(args).fl()
        path = [str(p) for p in path if p is not None]
        if len(path) == 0:
            return None

        path = [str(p) for p in path]
        return os.path.expanduser(os.path.normpath(os.path.join(path[0], *path[1:])))

    def rm(self, path_to_rm: str | list):
        path_to_rm = self.s(path_to_rm)
        if os.path.isdir(path_to_rm) and not os.path.islink(path_to_rm):
            shutil.rmtree(path_to_rm, ignore_errors=True)
        else:
            try:
                os.unlink(path_to_rm)
            except FileNotFoundError:
                pass

    def mm(self, path: str | list) -> Optional[str]:
        """returns the mime type of a file"""
        return mimetypes.guess_type(self.s(path))[0]

    def fn(self, path: str | list) -> str:
        """returns the filename of a path"""
        return os.path.basename(self.s(path))

    def _ensure_parent_exists(self, target_path):
        dirname = os.path.dirname(target_path.rstrip('/'))
        os.makedirs(dirname, exist_ok=True)

    def mkdir(self, path: str | list):
        os.makedirs(self.s(path), exist_ok=True)

    def cp(self, from_path: str | list, to_path: str | list, hardlink=False):
        # ensure parent directory exists
        from_path = self.s(from_path)
        to_path = self.s(to_path)
        self._ensure_parent_exists(to_path)
        if hardlink:
            if self.ed(from_path):
                shutil.copytree(from_path, to_path, copy_function=os.link, dirs_exist_ok=True)
            else:
                os.link(from_path, to_path)
        else:
            if self.ed(from_path):
                shutil.copytree(from_path, to_path, dirs_exist_ok=True)
            else:
                shutil.copy(from_path, to_path)

    def tree(self, path: str | list) -> dict:
        # returns the directory in a tree representation
        pass

    def ln(self, from_path: str | list, to_path: str | list):
        from_path = self.s(from_path)
        to_path = self.s(to_path)
        self._ensure_parent_exists(to_path)
        self.rm(to_path)
        os.symlink(from_path, to_path)

    def uz(self, zip_path, folder_path):
        if os.path.exists(folder_path) and not os.path.isdir(folder_path):
            raise IOError(folder_path + ' exists and is not a directory')
        os.makedirs(folder_path, exist_ok=True)
        shutil.unpack_archive(zip_path, folder_path)

    def ff(self, path):
        return os.path.basename(self.s(path))

    def sib(self, path, new_name) -> str:
        """returns the sibling file of a path"""
        path = self.s(path)
        if path.endswith('/'):
            path = path[:-1]
        return self.s(os.path.dirname(path), new_name)

    def w(self, path, contents, pretty=False):
        path = self.s(path)
        dirname = os.path.dirname(path)
        if len(dirname.strip()) != 0:
            os.makedirs(dirname, exist_ok=True)
        if isinstance(contents, str):
            with open(path, 'w') as f:
                f.write(contents)
        elif isinstance(contents, bytes):
            with open(path, 'wb') as f:
                f.write(contents)
        elif isinstance(contents, dict):
            with open(path, 'w') as f:
                if not pretty:
                    json.dump(contents, f)
                else:
                    json.dump(contents, f, sort_keys=False, indent=2)
        else:
            raise ValueError(contents)

    def rl(self, path: str | List) -> ImkList[str]:
        """reads the nonempty lines in a text file"""
        return ImkList([s.strip() for s in self.r(path, str).split('\n') if s.strip()])

    def fri(self, name):
        """returns a friendly file name for a name"""
        return re.sub(r'[^a-zA-Z0-9_.-]', '_', name)

    def r(self, path: str | List, t: Type[str | bytes | dict | list] = str):
        path = self.s(path)
        if t is None or t is str:
            with open(path, 'r') as f:
                return f.read()
        elif t is bytes:
            with open(path, 'rb') as f:
                return f.read()
        elif t is dict:
            with open(path, 'r') as f:
                return json.load(f)
        elif t is list:
            with open(path, 'r') as f:
                return list(csv.reader(f))
        else:
            raise ValueError(t)

    def rb(self, path) -> bytes:
        return self.r(path, bytes)

    def ls(self, path='.', regex=None, suffix=None):
        path = self.s(path)
        if not os.path.isdir(path):
            return []
        if isinstance(regex, str):
            regex = re.compile(regex)

        def should_incl_path(path):
            if regex is not None:
                if regex.search(path) is None:
                    return False

            if suffix is not None:
                if isinstance(suffix, str) and not path.endswith(suffix):
                    return False
                if isinstance(suffix, list) and not any(path.endswith(s) for s in suffix):
                    return False

            return True

        return [self.s([path, f]) for f in os.listdir(path) if should_incl_path(f)]

    def e(self, path: str | list) -> bool:
        if path is None:
            return False
        path = self.s(path)
        return os.path.exists(path)

    def sha1(self, path) -> str:
        return hashlib.sha1(self.r(path, bytes)).hexdigest()

    def wk(self, path: str | list, predicate: str = '*') -> 'ImkIoFileWalk':
        """walks through a directory, going through only files that fnmatch.match(predicate)"""
        return ImkIoFileWalk(self.s100, self.s(path), predicate)

    def one(self, path) -> str:
        """asserts there is only one meaningful file in this directory"""
        paths = self.wk(path).ll()
        paths = [p for p in paths if not p.endswith('.DS_Store')]
        assert len(paths) == 1, paths
        return paths[0]

    def ef(self, path: str | list) -> bool:
        if path is None:
            return False
        path = self.s(path)
        return os.path.exists(path) and os.path.isfile(path)

    def ed(self, path: str | list) -> bool:
        if path is None:
            return False
        path = self.s(path)
        return os.path.exists(path) and os.path.isdir(path)

    def txt(self, path: str | list) -> 'ImkIoTextEdit':
        return ImkIoTextEdit(self.s100, self.s(path))


class ImkIoFileWalk:
    def __init__(self, s100, path: str, predicate):
        self.s100 = s100
        self.path = path
        self.predicate = predicate

    def ll(self) -> ImkList[str]:
        return ImkList(self)

    def __iter__(self):
        for path, dirs, files in os.walk(os.path.abspath(self.path)):
            for filename in fnmatch.filter(files, self.predicate):
                filepath = os.path.join(path, filename)
                yield filepath

    def pr(self):
        for filepath in self:
            print(filepath)

    def e(self, trn):
        for filepath in self:
            with open(filepath) as f:
                s = f.read()
            s = trn(s)
            with open(filepath, "w") as f:
                f.write(s)


class ImkIoTextEdit:
    def __init__(self, s100, path: str):
        self.s100 = s100
        self.path = path

    def rp(self, old, new):
        with open(self.path, 'r') as f:
            content = f.read()

        content = content.replace(old, new)
        with open(self.path, 'w') as f:
            f.write(content)

        return self


class ImkIoInDir:
    def __init__(self, s100, path: str):
        self.s100 = s100
        self.path = path

    def s(self, path=None):
        return self.s100.py.io.s([self.path, path])

    def ymd(self) -> 'ImkIoInDir':
        datestring = time.strftime("%Y-%m-%d")
        return self.s100.py.io(self.s(datestring)).mk()

    def ls(self):
        return self.s100.py.io.ls(self.path)

    def rm(self, path):
        return self.s100.py.io.rm([self.path, path])

    def mk(self):
        os.makedirs(self.path, exist_ok=True)
        return self

    def wk(self) -> ImkIoFileWalk:
        return ImkIoFileWalk(self.s100, self.path, '*')

    def w(self, path, contents, pretty=False):
        path = self.s100.py.io.s([self.path, path])
        self.s100.py.io.w(path, contents, pretty)
        return self

    def r(self, path, t: Type[str | bytes | dict | list] = str):
        path = self.s100.py.io.s([self.path, path])
        return self.s100.py.io.r(path, t)

    def rb(self, path) -> bytes:
        path = self.s100.py.io.s([self.path, path])
        return self.s100.py.io.r(path, bytes)

    def e(self, path):
        path = self.s100.py.io.s([self.path, path])
        return self.s100.py.io.e(path)

    def cd(self, path):
        return ImkIoInDir(self.s100, self.s100.py.io.s([self.path, path]))

    def ln(self, from_path: str | list, to_path: str | list = None):
        """impression: walter from Hellsing"""
        if to_path is None:
            to_path = os.path.basename(self.s100.py.io.s(from_path))
        self.s100.py.io.ln(from_path, self.s100.py.io.s([self.path, to_path]))
        return self

    def reg(self, registry_save_path, predicate: str = '*'):
        assert registry_save_path.endswith('.json')
        return ImkIoInDirFileRegistry(self.s100, self.path, registry_save_path, predicate)

    def __str__(self):
        return self.path

    def __repr__(self):
        return str(self)


class ImkIoInDirFileRegistry:
    def __init__(self, s100, path: str, registry_save_path: str, predicate: str):
        self.s100 = s100
        self.path = path
        self.registry_save_path = registry_save_path
        self.predicate = predicate

    def known(self) -> list['ImkFileRegistryEntry']:
        if not self.s100.py.io.ef(self.registry_save_path):
            return []
        with open(self.registry_save_path, 'r') as f:
            return [ImkFileRegistryEntry(**e) for e in json.load(f)]

    def new(self) -> list['ImkFileRegistryEntry']:
        """returns the list of new sha1 entries"""
        found_sha1: set[str] = set(e.sha1 for e in self.known())
        entries = []
        for f in self.s100.py.io.wk(self.path, self.predicate):
            sha1 = self.s100.py.io.sha1(f)
            if sha1 not in found_sha1:
                found_sha1.add(sha1)
                entries.append(ImkFileRegistryEntry(path=f, sha1=sha1))
        return entries

    def add(self, entries: list['ImkFileRegistryEntry']):
        existing = self.known()
        found_sha1: set[str] = set(e.sha1 for e in existing)
        entries = [e for e in entries if e.sha1 not in found_sha1]
        if entries:
            entries = existing + entries
            with open(self.registry_save_path, 'w') as f:
                json.dump([asdict(e) for e in entries], f, indent=4)


@dataclass(frozen=True)
class ImkFileRegistryEntry:
    path: str
    sha1: str
