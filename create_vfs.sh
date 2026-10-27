#!/bin/bash
# Создаем минимальную VFS
mkdir -p minimal_vfs
touch minimal_vfs/file1.txt

# Создаем VFS с несколькими файлами
mkdir -p multi_vfs
touch multi_vfs/a.txt multi_vfs/b.txt multi_vfs/c.txt

# Создаем VFS с 3 уровнями вложенности
mkdir -p deep_vfs/level1/level2/level3
touch deep_vfs/root.txt
touch deep_vfs/level1/mid.txt
touch deep_vfs/level1/level2/deep.txt
