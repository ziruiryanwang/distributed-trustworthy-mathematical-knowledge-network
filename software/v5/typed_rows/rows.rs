//! Decoded syntax only: neither these rows nor their constructors carry authority.
//! Generic foundation/declaration rows retain their complete original Values.
use serde_json::Value;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Row {
    Legacy(Value),
    Dag(DagRow),
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DagBinderStyle { Default, Implicit, StrictImplicit, InstImplicit }

impl DagBinderStyle {
    pub fn as_str(self) -> &'static str {
        match self {
            Self::Default => "default", Self::Implicit => "implicit",
            Self::StrictImplicit => "strictImplicit", Self::InstImplicit => "instImplicit",
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum DagRow {
    NameStr { index: u32, pre: u32, text: String },
    NameNum { index: u32, pre: u32, value: u32 },
    LevelSucc { index: u32, child: u32 },
    LevelParam { index: u32, name: u32 },
    LevelMax { index: u32, left: u32, right: u32 },
    LevelIMax { index: u32, left: u32, right: u32 },
    ExprBVar { index: u32, value: u16 },
    ExprSort { index: u32, level: u32 },
    ExprConst { index: u32, name: u32, levels: Vec<u32> },
    ExprApp { index: u32, fun: u32, arg: u32 },
    ExprLambda { index: u32, name: u32, ty: u32, body: u32, binder: DagBinderStyle },
    ExprPi { index: u32, name: u32, ty: u32, body: u32, binder: DagBinderStyle },
    ExprLet { index: u32, name: u32, ty: u32, value: u32, body: u32, nondep: bool },
    ExprProj { index: u32, type_name: u32, field: usize, structure: u32 },
}

impl DagRow {
    pub fn domain(&self) -> &'static str {
        match self {
            Self::NameStr { .. } | Self::NameNum { .. } => "in",
            Self::LevelSucc { .. } | Self::LevelParam { .. }
                | Self::LevelMax { .. } | Self::LevelIMax { .. } => "il",
            _ => "ie",
        }
    }

    /// Syntax assembly only. Ordered reference/domain validation happens later.
    pub fn with_index(mut self, new_index: u32) -> Self {
        let slot = match &mut self {
            Self::NameStr { index, .. } | Self::NameNum { index, .. }
            | Self::LevelSucc { index, .. } | Self::LevelParam { index, .. }
            | Self::LevelMax { index, .. } | Self::LevelIMax { index, .. }
            | Self::ExprBVar { index, .. } | Self::ExprSort { index, .. }
            | Self::ExprConst { index, .. } | Self::ExprApp { index, .. }
            | Self::ExprLambda { index, .. } | Self::ExprPi { index, .. }
            | Self::ExprLet { index, .. } | Self::ExprProj { index, .. } => index,
        };
        *slot = new_index;
        self
    }
}
