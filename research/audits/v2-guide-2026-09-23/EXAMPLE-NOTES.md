# v2 guide: checked Rose/count teaching notes

2026-09-23. Independent documentation subtask. Canonical root guard passed via the documented process-local ExecutionPolicy Bypass invocation. Read-only inspection of retained source and outcome evidence; no product edit, import, execution, experiment, build or network call. This file is the assigned checkpoint. The scope is frozen delivered source13; unfinished source14 is excluded.

## Sources actually read

- `AGENTS.md`, `GOAL.md`, authoritative current portion of `research/NOW.md`.
- `experiments/auxiliary-frontend-01/EXERCISE-OUTCOME.md`.
- `experiments/auxiliary-frontend-01/CONTINUATION-OUTCOME.md`.
- `experiments/auxiliary-frontend-01/consumer/CountPublishable.lean`.
- `experiments/auxiliary-frontend-01/reciprocal-01/Rose.lean`.
- `experiments/auxiliary-frontend-01/reciprocal-01/SOURCE13-PUBLIC-INTERFACE.json`.
- `deliverables/2026-09-23-v2-local-release/QUALIFICATION.md`.
- Supplementary original-source derivation: `experiments/public-group-roots-01/consumer/AUTHOR.md`. Its old not-yet-verified status is superseded only by the separate actual outcome audits, not silently rewritten.

## Suggested undergraduate explanation in Chinese

### 1. 先认识要交换的数学对象

实际生产者提交的 Lean 源码只有这一行：

```lean
inductive Rose where | node : List Rose -> Rose
```

`Rose` 是一类有限树的类型；这里的树没有额外的节点标签。`List Rose` 是一个有限、按顺序排列的子树列表。`node` 把这样的列表接到一个新根节点下面，得到一棵树。每个节点可以有零个、一个或多个子节点，因此它不是限定两个孩子的二叉树。

`node []` 是一个没有孩子的叶节点，仍然有一个节点。这个类型没有另设“空树”构造。`[]` 是空的树列表，并非一棵零节点的 Rose 树。这是解释计数时最容易遗漏的区别。

把一个树列表称为“森林”只是教学术语；实际源码使用已有的 `List Rose`，没有另外定义一个 Forest 数据类型。树和森林的关系如下：一棵树是“一个根 + 一片孩子森林”；一片森林是“空列表”，或“一棵首树 + 剩下的森林”。

### 2. 为什么只收到类型名字还不够

为了使用一个归纳类型，我们需要知道如何构造它，也需要知道如何按其结构计算或证明。可以把 recursor（递归/归纳原理）理解为 Lean 为这种数据结构配套提供的一套受检查的结构处理规则。给出各个构造情形的处理办法，它就能把任意这类对象处理完。

对 Rose 而言，递归发生在 `List Rose` 内部：先处理孩子森林，再处理根节点；处理森林时又要处理其中每一棵树。因此实际收到的检查接口包含四项：树类型、节点构造器、以树为输入的主 recursor、以树列表为输入的辅助 recursor。辅助 recursor 在这个例子里的公开名字后缀是 `t0.rec_1`，主 recursor 是 `t0.rec`。

这里的“辅助”是处理嵌套列表所需的正式递归入口，不是一个可以忽略的备注。source12 曾经能在内核里重建它，也能把它列在接口中，却未把它正确登记到普通 Lean 源码使用的前端名字表里。结果消费者写源码引用它时得到 unknown constant。source13 修复了这一处可用性缺口；它没有放宽数学检查，也没有凭空制造新公理。

### 3. 消费者怎样定义计数

消费者新建两个函数：`nodeCount : Rose → Nat` 数一棵树的节点总数；`forestCount : List Rose → Nat` 数一片森林里全部树的节点总数。

下面是帮助理解的数学规则/伪代码，**不是本次实际提交的 Lean 源文件，也没有作为新程序重新执行**：

```text
nodeCount(node(xs)) = 1 + forestCount(xs)
forestCount([]) = 0
forestCount(t :: ts) = nodeCount(t) + forestCount(ts)
```

其中 `t :: ts` 表示把树 `t` 放在列表 `ts` 的前面。第一条给根节点计 1，再加所有孩子的节点数；第二条说空森林没有节点；第三条把列表首项与剩余项的节点数相加。

实际测试源码直接应用收到的两个 recursor：`nodeCount` 用主 recursor，`forestCount` 用辅助 recursor。两者给出的结果类型都是 `Nat`，处理办法相同：节点情形把孩子已经算出的总数 `n` 变为 `Nat.add 1 n`，空列表情形给 `0`，非空列表情形把首树结果 `n` 与剩余森林结果 `m` 相加。

实际源码中的 `fun _ : Rose => Nat` 和 `fun _ : List Rose => Nat` 是这两个结果类型的说明。一般递归原理允许结果类型依赖输入对象；这里没有这种依赖，不论输入是什么，结果类型都是自然数。初读时可把它们理解为“树处理完得一个自然数；森林处理完也得一个自然数”。

实际定义使用 `noncomputable def`。这不表示“数树节点在数学上不可计算”。它使这条源码路径不必为按规范名字重建的定义生成可执行程序代码；Lean 内核仍然能依据定义和递归计算规则检查下面的等式。不要把内核的定义展开与运行一个编译后的计数程序混为一谈。

### 4. 手算几个小例子

以下记号和数值是教学上的手算实例，不是新增的运行测试记录。令 `leaf = node []`，`branch = node [leaf]`。

| 对象 | 形状 | 节点总数 |
| --- | --- | ---: |
| `leaf` | 单个叶节点 | 1 |
| `branch` | 一个根接一个叶节点 | 2 |
| `node [leaf, leaf]` | 一个根接两个叶节点 | 3 |
| `node [leaf, branch]` | 一个根接一个叶节点和一棵两节点的树 | 4 |
| 森林 `[leaf, branch]` | 并列放置上面的两棵树，没有添加共同根 | 3 |

最后两行区别很重要：森林只把现有的树放在一起；`node` 还会增加一个根。

### 5. 实际通过的定理是什么

实际定理名为 `countEquations`，对任意一棵收到的 Rose 树 `t`，同时断言两件事：

1. `forestCount [t] = nodeCount t`：只放一棵树的森林，其总数就是这棵树的节点数。
2. `nodeCount (roseNode [t]) = Nat.add (Nat.succ Nat.zero) (nodeCount t)`：给这棵树外面再加一个根，节点数增加一。

`Nat.zero` 是自然数 0，`Nat.succ` 是取后继，所以 `Nat.succ Nat.zero` 表示 1。`roseNode` 是实际消费者源码对收到的节点构造器所设的局部记号，并没有重新定义一套树。

这两条是关于所有 `t` 的一般命题，不只是检查上表中的几个样本。但它们属于定义直接给出的计算规律，不是一个需要新数学思想的深定理。

实际证明是：

```lean
  And.intro
    (Eq.refl (forestCount [t]))
    (Eq.refl (nodeCount (roseNode [t])))
```

`And.intro` 把两个证明合为“并且”的证明；`Eq.refl x` 是“x 等于它自己”的证明。为什么这种证明能对应表面上不同的两边？因为 Lean 会把定义展开到足以比较的程度。

第一条左边依次展开为 `nodeCount t + forestCount []`，再变为 `nodeCount t + 0`，最后变为 `nodeCount t`。第二条左边展开为 `1 + forestCount [t]`，再变为 `1 + nodeCount t`。这与右边 `Nat.add (Nat.succ Nat.zero) (nodeCount t)` 表示的是同一个定义性计算结果。这里不需要知道未知树 `t` 到底有多少节点，也不需要先对 `t` 做另一套归纳证明。

### 6. 为什么这个小定理对项目仍有价值

测试要验证的关键是软件能否保存并实际使用数学接口：A 提交并发布 Rose 类型；B 发现、取得并在自己的节点重新检查该类型；B 在收到的精确类型上定义两个计数函数并证明方程；B 发布这个新贡献；A 取得它，并在 B 的有限服务已停止之后，使用已取得的本地包重新进行数学准入检查。

审计不只找到了“定理正文里提到 Rose”这类文字证据。它检查了完整源表达式与规范对象的一致性，并沿实际证明值的依赖走到了两个计数定义，再走到收到的主 recursor 和辅助 recursor。这说明接收方实际使用了收到的结构计算规则。

因此它有分量的地方是“真实的类型/递归接口交换和双向复用链路通过了这个具体例子”。这个结果并不证明系统已经产生有用的新数学、广泛支持数学库、优于本地库工作，或者能长期持续积累知识。本次是同一物理机器上两个节点的、非盲测的工程演示。

### 7. 原来的数字 1 为什么会导致失败

原始版本的定理右边写成 `Nat.add 1 (nodeCount t)`。source13 的实际数学提交已经接受了它：源捕获、规范转换、新的原生检查、逆向导出和再次检查均通过。然而随后的 `publish` 拒绝了它，错误为 `CANDIDATE_TYPE_FRAGMENT:NATIVE_SYNTAX_OUTSIDE_TYPE_FRAGMENT`。

原因在发布时构建的类型符号索引：交付的 source13 索引只接受变量、Sort、常量、应用、lambda 和 Pi 等类型表达式节点（标签 0–5）。原始定理类型中的 `1` 被编码为一个自然数字面量节点，超出这段已支持的语法。它是索引/发布支持范围的限制，不是证明有错，也不是辅助 recursor 仍不可用。

后续工作只改了定理陈述中这一个位置，写成 `Nat.succ Nat.zero`，让这个定理类型由已支持的常量和应用等节点表示。两个计数定义，包括它们定义体内的 `1` 和 `0`，以及两个证明都未改变。所以上述规则中的普通 `1` 可作为教学数学记号，但展示“实际成功提交的 theorem 源码”时应保留构造器写法。

数学意义和定义性计算相同，并不表示规范语法字节相同。修改后的定理有不同的类型编码和内容标识，经过自己的重新提交、检查、发布、TLS 返回传输和 A 的重新准入检查后才通过。不能说系统自动规范化了原定理，不能说原先被拒绝的那次发布后来变成成功，也不能把 source14 的在研改动算作 v2 已交付能力。

## Precise evidence anchors for the main guide

- Actual Rose source: `experiments/auxiliary-frontend-01/reciprocal-01/Rose.lean` (one line).
- Actual successful continuation source: `experiments/auxiliary-frontend-01/consumer/CountPublishable.lean` (25 lines, 1,152 bytes, SHA-256 `fc49d2505136a19cc2352abddf8303b6a0c9e279d3c39e82b77d2691fc4cbb71`). The theorem starts at line 20; count definitions start at lines 4 and 12.
- Main recursor selector `[2,0]`; auxiliary recursor selector `[3,1]`; exact public source references are in `SOURCE13-PUBLIC-INTERFACE.json`.
- Original exercise: `EXERCISE-OUTCOME.md`, disposition `RETAINED_PUBLICATION_FRAGMENT_FAILURE_WITH_ACTUAL_AUXILIARY_SOURCE_ACCEPTANCE`.
- Successful continuation: `CONTINUATION-OUTCOME.md`, disposition `PASS_SELECTED_SOURCE13_SOURCE_ONLY_RECIPROCAL_CONTINUATION`.
- Continuation capture reaches exactly three new source units: `nodeCount`, `forestCount`, `countEquations`. Six other declarations are omitted as unreached. Candidate/inverse/retained/acquired packages have matching exact 24-file maps.
- The two definitions remain identical across the original/continuation. `nodeCount` definition digest: `81802af3c8411743ec48968c09137b62de51e8307155e9c7f8eeefc34450a5a9`; `forestCount`: `493051972bc198f0ad9e9600e27def69ae05711dddaa3e22cd8b8cfbb49997f7`.
- The new theorem statement uses only tags 0, 2, 3 and 5; its PI digest is `703925417aac7957147edaff73c0dbcf734efb4ad11572aaf637dcd2c6d15d41`.
- Continuation itself adds six ordinary calls: B submit/publish/expose, A peer_find/peer_acquire/admit. Two new native stages; no rebuild, reinitialization or renewal.
- Original plus continuation: 16 attempted/15 successful ordinary requests, seven native stages and two publications (Rose and revised Count). Original failure remains retained and charged.

## Review pitfalls

1. Do not call Rose a binary tree, an arbitrary labeled tree, an infinite tree, or a zero-node empty tree type.
2. Do not say the consumer redefined Rose. Its local notations reference the exact acquired type/constructor.
3. Do not present the three explanatory counting equations as the tested source code. The tested definitions are direct recursor applications.
4. Do not describe the theorem as “counting every tree by enumeration”, a new discovery, or deep induction. It is universal but proved by definitional computation.
5. Do not reduce the engineering result to a name/type occurrence. The actual term dependency audit reaches both recursor values.
6. Do not say all numeral use failed: the blocked node is in the theorem type used for publication indexing; unchanged definition bodies retain literals.
7. Do not conflate native/kernel acceptance with publication, TLS receipt with mathematical acceptance, or archived status with fresh checking.
8. Do not call the successful type encoding the same content ID as the original one. Definitional equivalence does not merge byte identities here.
9. Do not include source14 support as delivered v2. Do not imply independent physical hosts, blinded autonomous research, useful growth or comparative efficiency.

## Final guide review disposition

Reviewed `deliverables/2026-09-23-v2-guide/GUIDE.md`, 46,875 bytes, SHA-256
`52ff403318c9ca14bdf69eb333b99eaa8a0899ecfe217b8f6b45a46210f55445`.
The primary scope is the complete Layer 5 (lines 333–463), with the nearby
mathematical trust, representation, submission and evidence explanations
(Layers 2–4 and 10). Read actual `CountPublishable.lean` again and compared
against the outcome records read above. No product execution or edit occurred.

Disposition: **PASS_MATHEMATICAL_EXAMPLE_DOCUMENTATION_REVIEW**. No blocking
mathematical inaccuracy or overstated experiment conclusion was found within
this scope. This is documentation review, not a new software qualification.

The guide correctly distinguishes ordered finite Rose trees from forests,
explains the main/auxiliary recursion roles, labels the counting equations as
explanatory rather than executed source, states both universal equations,
identifies their definitional/reflexivity proof, and grounds actual reuse in
proof-value dependencies. It also separates accepted original mathematics from
failed publication, preserves the distinct revised identity, states that the
definition-body literals remain, and excludes source14 and broad-growth claims.
The conditional trust explanation and source/canonical/fresh-check discussion
are consistent with those boundaries.

Two optional clarity improvements were sent to the root; neither is required
for mathematical correctness:

1. At line 426, replace “Both counting definitions survived into the returned
   theorem's statement” with “The returned theorem's statement referred to
   both counting definitions.” This avoids suggesting that both complete
   function bodies occur literally in the proposition.
2. After lines 411–415, a short reduction example can make reflexivity easier
   for a first-time reader: `forestCount [t]` reduces to `nodeCount t + 0`,
   then to `nodeCount t`; `nodeCount (node [t])` reduces to
   `1 + forestCount [t]`, then to `1 + nodeCount t`. These are explanations
   of the audited definitions, not new executed tests.

Only this assigned review file was edited. The root-owned guide was not edited.
