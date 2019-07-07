#!/bin/bash

cd ~/sdk || exit 1
echo "CONFIG_DEVEL=y" > .config
echo "CONFIG_SRC_TREE_OVERRIDE=y" >> .config
make defconfig
./scripts/feeds update base
ln -s "$CI_PROJECT_DIR/.git/" ~/sdk/feeds/base/package/network/config/firewall/git-src
./scripts/feeds install firewall
make package/firewall/{clean,compile} -j"$(nproc)" || make package/firewall/compile V=s
