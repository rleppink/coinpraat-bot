with import <nixpkgs> {};

stdenv.mkDerivation {
    name = "coinpraat-bot";
    buildInputs = [
        python36
        python36Packages.requests
        python36Packages.yapf
        python36Packages.tzlocal
    ];
    shellHook = ''
        alias run="python src/main.py"
    '';
}
