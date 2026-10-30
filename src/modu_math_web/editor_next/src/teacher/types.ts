export interface User { id: number; username: string; role: "admin" | "teacher" | "student"; is_active?: boolean }
export interface Page<T> { count: number; next: string | null; previous: string | null; results: T[] }
export interface Student { id: number; user_id: number; username: string }
export interface Classroom { id: number; name: string; teacher: number; invite_code: string; archived: boolean }
export interface Enrollment { id: number; classroom: number; student: number; username: string; status: "pending" | "approved" | "inactive" }
export interface Problem { id: number; problem_id: string; title: string; language: string; grade: number | null; problem_type: string; concepts: string[]; unit: string; path: string; file_prefix: string; publication_status: string; difficulty: number }
export interface ProblemDetail extends Problem { semantic_data: Record<string, unknown>; renderer_data: Record<string, unknown>; answer: unknown }
export interface ProblemSet { id: number; title: string; description: string; version: number; items: { problem: number; position: number }[] }
export interface Assignment { id: number; title: string; problem_set: number; source_version: number; status: "active" | "closed" | "cancelled"; starts_at: string | null; due_at: string | null; max_attempts: number; release_policy: string; item_count: number; recipient_count: number; submitted_count: number; accuracy: number }
export interface Recipient { id: number; recipient_id: number; student_id: number; username: string; total: number; completed: number; progress: number; submitted_at: string | null; correct: number; accuracy: number; elapsed_ms: number; hint_count: number; wrong_item_ids: number[] }
export interface Results { assignment: Assignment; recipients: Recipient[]; items: { item_id: number; position: number; answered: number; correct: number; accuracy: number; elapsed_ms: number; concepts: string[] }[]; concepts: Record<string, { correct: number; total: number }>; unsubmitted_recipient_ids: number[] }
export interface Dashboard { students: number; classes: number; assignments: number; recipients: number; submitted: number; unsubmitted: number; statistics_scope: string }
export type Section = "dashboard" | "bank" | "sets" | "assignments" | "students" | "classes" | "results";
