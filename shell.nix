with import <nixpkgs> {};

stdenv.mkDerivation {
    name = "coinpraat-bot";
    buildInputs = [
        python36
        python36Packages.pyyaml
        python36Packages.requests
        python36Packages.tzlocal
        python36Packages.munch
        python36Packages.python-Levenshtein

        python36Packages.flake8
        python36Packages.yapf
    ];
    shellHook = ''
        alias run="python coinpraat-bot/main.py"
    '';
}
