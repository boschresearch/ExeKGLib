# Contributing

## TL;DR: 10 Steps To Your First Pull Request

Ok, this is a long document so let's TL;DR this. The following recipe quickly outlines ten steps to your first
successful contribution in the form of a pull request.

1. First, create an issue in our [issue tracker][issues] and describe the contribution you intend to make.
2. We use feature branches. So before you start coding, create a fork and a local feature branch, on which you will make
   your changes. We use the following template for naming feature branches: `"feature/"<Short description>`
   Here is an example for a valid feature branch name: `feature/enhance-documentation`
   ([More about our branching conventions](#branching-conventions))
3. Make the changes in your local git repository and commit.
   ([More about our commit message conventions](#commit-message-conventions))
4. When you'd like to share your code and/or start a pull request to get feedback, push your commits to the repository.
5. Open the _Branches_ view in GitHub. Your newly pushed branch should show up there. Usually, all repositories have an
   associated build job which will pick up your new branch and build it once you open a PR.
6. If the build fails and you know how to fix it, please do. If you don't, go ahead and contact us via the pull request
   to allow us to help you make the build green.
7. Enter a meaningful title, prefixed with the issue number and possibly a slightly longer version of your branch name.
   Here is an example: `#1 - Add missing documentation`
8. Briefly describe the changes you are submitting in the _Description_ field. The goal here is to make the life of the
   reviewers as easy as possible by explaining what you did and why. The description can be formatted as markdown, so
   feel free to format, add code examples, link to specific lines of code or even add sketches or diagrams. You can also
   @-mention anyone on GitHub to inform them of the PR (usually we do that by prefixing the @-mention with `/CC` or `/FYI`).
   ([More on our conventions for communicating within pull requests](#conventions-for-communicating-in-pull-requests))
9. Every pull request will be reviewed and approved by at least one maintainer (see `README.md`) before it is merged.
10. Add at least one of the maintainers as reviewer.

This is, in a nutshell, how you make contributions to this community. It may sound complicated at first, but you'll
quickly internalize the steps and will be able to create a pull request in mere minutes or less. Please find a detailed
description in the [_How to Contribute_](#how-to-contribute) section.



## Whom to Contact in Case of Questions?

Communication is usually done via Issues and PRs. If, for some reason, you prefer kicking off the collaboration in a
personal conversation, please contact the maintainers of this repository, which are listed in this repository's `README.md`.

## How to Submit a Bug Report?

Found a bug? Great! A core task in improving our product is to identify any flaws that may be present. The best place to
report a bug is to [create an issue in our issue tracker][issues].

## How to Submit a Feature Request?

If you have suggestions for us on how to improve our code or our documentation or have a new feature in mind, please by
all means do let us know.
The same rules apply as for bug reports: add a new issue outlining your suggestion in our [issue tracker][issues].

## How to Contribute?

If you have fixed a bug or have developed that new feature you would like to make available to your fellow users, or
even if you have fixed whitespace or formatting issues, we'd like to encourage you to contribute that to our codebase.
In this repository, we use [pull requests](#pull-requests) to facilitate all contributions. Every pull request will be
peer-reviewed by at least one community member, which is a great way to get in touch with each other.

### Clean Code

More important than writing code that adheres to our styleguide is writing _Clean Code_. We consider code to be _clean_,
if it

- works,
- is easy to understand,
- is easy to modify and
- is easy to test.

Any code contribution will be reviewed by us with respect to these criteria. We are more than happy and indeed consider
it a core part of _being BIOS_ to invest time mentoring junior developers to help them create _cleaner_ code and to
improve future contributions.

In addition to these principles of clean code, we also try to _design our architectures for participation_.
That, to us, means to avoid unnecessary complexity, tight coupling or complex dependency relationships.

### Testing Conventions

We are convinced that writing testable code and writing tests is a precondition for any software to be maintainable.
Even though we do not prescribe fixed coverage thresholds for our tests, we encourage (and often will require) you to
write tests for code that needs to be maintainable where the effort is not excessive. This means, that we

- aim to write code with testability in mind (following the test first principle)
- write tests for everything we can test
- expose a submitted bug with a test first, before we implement a fix.

We also aim to write our tests such that they can be read as a specification (because we usually don't spend time
writing those). In practice, this means that we use long, verbose and expressive names for tests which convey the
condition being tested.

In our experience, writing tests can actually be a lot of fun.
As a programmer, you have more leeway to experiment and try new programming approaches when writing tests.
That is why we often try out new language features in our test code, first.
And if you're following the test first principle, it's always quite rewarding to see those red test cases continue to
turn green, once the implementation is complete. Finally, only adequate tests will empower you to continuously improve
your codebase with refactoring, as this provides the reassurance that you didn't break anything accidentally.

### Branching Conventions

The following convention applies for naming feature branches:

    feature/<description>

Here is an example for a valid feature branch name:

    feature/add-missing-docstrings

### Commit Message Conventions

We follow the [conventional commits][conventionalcommits] specification to add human and machine readable meaning to
commit messages. In general, commit messages should briefly describe the change introduced with the commit and ideally
contain the issue id(s) the changes refer to. Here are some examples of good commit messages:

    "feat(docs): added installation instructions for getting started (#1)"
    "fix(module-a): Added missing arguments in docstrings (#2)"

Following this convention automatically associates the commit, and thus the branch and pull request that it belongs to
with the given issue and vice versa.

### Writing Documentation

We follow these principles when documenting code:

- We aim at keeping documentation as close the the asset being documented as possible. That is, where sensible, we use
  inline code documentation.
- We use [Mermaid] for specifying diagrams in the code in order to be tool agnostic and allow everybody to adapt and
  improve it.
- We favor [Markdown][markdown] or other text based means of generating documentation and try not to use proprietary
  tools, such as Word or PowerPoint for that.
- We aim at providing our users with easy to understand instructions on how to use our code in each repositories `README.md`.
- We favor code examples over analytical descriptions of our codebase.

### Pull Requests

Pull requests are our main vehicle for submitting, reviewing and merging new code into our codebase. A pull request is
more than just an easy interface to git: it is a powerful collaboration and communication tool. They are especially well
suited to share knowledge and onboard new contributors. So if you are new to te community, submitting pull requests is
an excellent way for you to engage with us and for us to help you get started. Discussions and the Q&A that often
accompanies pull requests are archived and linkable and we thus use them to disseminate knowledge about our codebase.

#### Conventions for Communicating in Pull Requests

These articles ([1][anatomy-of-a-perfect-pull-request], [2][code-review-love]) summarize how (and how not) to
communicate in pull requests. Apart from the social aspects of interactions, we follow a couple of conventions for
signaling, i.e. using the various technical means of communicating in pull requests that are afforded to us by GitHub.

Below are common signals and how you use our platform to set them.

| Signal                                                        | Description                                                                                                                                           |
| :------------------------------------------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Add s.o. as reviewer**                                      | _"I'd like you to review my PR and I will not merge w/o your approval!"_                                                                              |
| **Approve a PR**                                              | _"I'm ok with merging this PR. If there are open tasks, I expect these to be finished before merging and I trust you to do this w/o another review!"_ |
| **PR Needs Work**                                             | _"I am not ok with merging this PR and I require changes to be made. I will re-review this PR after changes are made!"_                               |
| **@-mention s.o. in PR description with /CC prefix**          | _"I'd like you to have a look at this PR but I'm not asking for your formal approval!"_                                                               |
| **@-mention s.o. in PR description with /FYI prefix**         | _"Just so you know, we're working on this!"_                                                                                                          |
| **@-mention s.o. in comment as part of question**             | _"Can you please reply to my question with a comment?"_                                                                                               |
| **Reviewer adds task to PR**                                  | _"This needs to be fixed before I merge this PR!"_                                                                                                    |
| **Author of PR adds task in response to comment of reviewer** | _"I will finish this** task before merging!"_                                                                                                         |
| **Mark task as completed**                                    | _"This task is finished and I have pushed the changes!"_                                                                                              |
| **Add like**                                                  | _"I agree with the statemens made in the liked comment!"_                                                                                             |
| **Add link to issue**                                         | _"I wil not make the change in this PR but will take care of it later!"_                                                                              |

Generally speaking, when signalling, try to

- be respectful,
- be concise,
- be specific,
- clearly state your expectation and
- use links where possible (to files, lines in files, commits, pull requests, people, issues, other comments, …)

#### Definition of Done

We use the following checklist to determine if a PR is ready to merge:

- The last build is _green_
- If new code was added or if a bug was fixed, corresponding tests have been added
- All tasks added by reviewers are resolved
- At least one maintainer has approved the PR and none has signaled _Needs Work_

#### General Tips

- Keep your PRs as small as possible. The smaller the PR the higher the velocity of review and acceptance.
- Avoid conflating multiple issues in one PR.
- Aside from that usually leading to huge PRs and it making the job of a reviewer unnecessarily harder, it will also
  confuse the automated T&R issue state transition feature we use.
- Write a good description to allow the reviewer to quickly get an overview of your changes.
- Don't add more than two reviewers if you expect all of them to review. This will most likely block you.

## Other Contributions

You don't have to be a coder to make a valuable contribution to this community! There are many contributions that you
can make as a non-coder that will be very valuable to the community, such as

- giving feedback of any kind,
- reporting bugs,
- requesting features,
- adding new or improvements existing documentation,
- helping other users to use our software,
- asking and/or answering questions in our forums,
- promoting BIOS, Social Coding, our community and our software within Bosch or
- designing artwork for both our software, our wiki or our Bosch connect presence.

_May the source be with you!_

<!-- URLs -->
[anatomy-of-a-perfect-pull-request]: https://hugooodias.medium.com/the-anatomy-of-a-perfect-pull-request-567382bb6067
[code-review-love]: https://mtlynch.io/code-review-love/
[conventionalcommits]: https://www.conventionalcommits.org/
[innersourcecommons]: https://innersourcecommons.org/
[issues]: https://github.com/boschresearch/ExeKGLib/issues
[markdown]: https://github.github.com/gfm/
[mermaid]: https://mermaid-js.github.io/mermaid
