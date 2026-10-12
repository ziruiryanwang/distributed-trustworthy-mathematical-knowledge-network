# Preserved invocation failure, not a compiler failure

Root selected claims-build01 f7a0dc98 after source/input review, then mistakenly
invoked the builder with the product runtime used by local controls instead of
the inherited build recipe's D:\Python314\python.exe. The process failed at
build_native.py:79 with ValueError: PINNED_PYTHON, exit1, reported wall0.8308567s.
No build directory or attempt record exists; no compiler/test/guest/proof ran.
This command's CPU was not separately instrumented and is not counted as zero.

Exact failed command (canonical workdir was supplied):

    product-local/v4-library-commons-02/commons-v4/receiver/runtime/python/python.exe
      -I -S -B software/v5/aggregate_claims/build_native.py
      experiments/v5-local-checks/aggregate-claims-build-01-selection.json
      f7a0dc9891a79817fab9bc318e2eaeeaf091413bc192d0dbb664d0ca118e236a

The refusal protected the selected execution profile. Provision source lines24-26
requires D:\Python314\python.exe (SHA25603168c01b7b7491423350e82c26fee71f35b43694d1319d3c668bda6903a0c38)
and python314.dll (SHA256fde89cdb5c2d08ae65de7ef4abca1876c93ba3796002f5ac0bf7e4d4f5a94da0).
Root proposes fresh claims-build02 with unchanged selected sources and budgets,
only the corrected invocation and fresh outputs; independent exact review must
precede it. Old selection01 is not retried or relabeled. All source bytes used
by the failed invocation stay frozen; no implementation fix is required.
