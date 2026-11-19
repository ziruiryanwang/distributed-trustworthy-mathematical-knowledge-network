# Democratization of Mathematics

**A shared library of mathematics that people and AI programs can build together.**

We are building software that helps people use each other's mathematical work.
Someone finds a useful result, checks its proof, builds on it, and shares what
they discover. The next person can start from there.

The long-term aim is a library spread across independently run computers.
People choose their own questions and share work without depending on a single
central server.

**Current status:** this is a research prototype. The code and research notes
are public, but the full system is still being developed. There is no
ready-to-install public release yet.

## Why build this?

Mathematics grows when people build on earlier ideas. Finding the right result,
checking its assumptions, and using it in a new proof can take substantial work.
AI programs can help with research, but they can also make mistakes.

We want useful discoveries to become easier to find, check, and reuse. That
includes new definitions and whole theories, as well as individual proofs.
Everyone can work on their own interests while giving others a better starting
point.

## A simple example

Imagine this collaboration:

1. Alice proves that a method merges two sorted lists of numbers into one list,
   still in numerical order and containing the same numbers.
2. Bob finds her result and checks its proof on his computer.
3. He uses it to prove that a sorting method works, then shares his proof.
4. Someone else can use both results in a larger piece of work.

The project aims to support this cycle across many people and AI programs:

**Find useful work → check it → build on it → share the result.**

## How the mathematics is checked

The project uses [Lean 4](https://lean-lang.org/), a language and tool for writing
mathematics in a form a computer can check. A **proof** explains why a claim
follows from its definitions and assumptions. Lean makes those details precise
enough to check by rules.

Your computer checks a proof before accepting the result for use. Search helps
you find work that might help; the proof checker checks its reasoning. A claim
from an AI program goes through the same checking rules as a claim from a person.
People or separate AI tools supply the ideas and proofs.

Passing these checks does not tell us whether a result is interesting or useful.
That is a separate problem. People and their programs choose what to investigate
and which results to use.

## What exists today

**The local prototype has demonstrated the complete research loop: find a result,
check it, build on it, share the new work, and have another participant check it.**

In a [completed demonstration](software/v5/ordinary_finite_map_refinement/ADOPTION.md),
one participant used shared results about table updates to develop new
mathematical definitions and proofs. A second participant independently checked
that work, used it to prove another theorem after the original provider stopped,
and returned the theorem for the first participant to check. Each participant
kept its own mathematical collection; the exchange ran on one computer.

The software also provides:

- **Search using familiar mathematical names.** Participants can find unfamiliar
  results by searching for mathematical objects they already use.
- **A growing local library.** Checked work stays available for later use, so
  participants can build further results without starting their collection over.
- **Separate storage and search services.** A lightweight
  [Python host](software/v5/ordinary_inert_host_role/ADOPTION.md) can accept and
  serve new contributions without rebuilding its whole collection. People using
  those contributions check the mathematics themselves.

The next development steps build on these working capabilities:

- **Handle larger collections and more providers:** improve search across them
  and reduce the cost of checking supporting mathematics on first use.
- **Make it easier to run on separate computers:** simplify setup and test the
  same exchange between independently operated machines.
- **Measure the benefit of sharing:** compare the time and computing cost of
  developing further mathematics with an equally capable standalone Lean project,
  including the costs of searching, checking, and sharing.

## Where to start

You can read about the project without installing anything:

- [Current design](CURRENT-DESIGN.md): how the parts fit together and what remains
  unfinished. This is the more technical explanation.
- [Project goals](GOAL.md): what we are working toward.
- [Source code](software/v5/): prototype code and tests.
- [Earlier versions and results](deliverables/): the project's development history.

<details>
<summary>For programmers: setup and current limits</summary>

The current development version is called v5. Its supported setup is Windows
x86-64, Python 3.14.6, and Lean 4.34.0.

The [current setup guide](software/v5/ordinary_owned_acquisition/kit/GUIDE.md)
explains the workflow and how to build from source. Its examples assume an
extracted development kit. That prebuilt kit and the required runtimes are not
included here. Setup from a Git checkout still requires manual work and matching
runtimes; the guide's paths must be adapted to your checkout.

The [current source builder](software/v5/ordinary_owned_acquisition/build.py)
and [record of the latest tested setup](software/v5/ordinary_owned_acquisition/ADOPTION.md)
identify the code used in development. Older notes may describe earlier versions
or link to files kept only on the development computer. [Version-control notes](VERSION-CONTROL.md)
explain which files are included in this repository.

</details>

The repository's full name is **Distributed Trustworthy Mathematical Knowledge
Network**. The source is public; a license has not yet been selected.
