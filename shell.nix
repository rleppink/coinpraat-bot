with import <nixpkgs> {};

(python36.withPackages
  (ps: with ps; [ flask requests tzlocal yapf ])).env
