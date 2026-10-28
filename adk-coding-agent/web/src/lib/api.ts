export type Status = {
  model: string
  llm_configured: boolean
  sandbox: string
  skills: number
  files: number
  sessions: number
}

export type Skill = { name: string; description: string; source: 'local' | 'vendor' }
export type DocFile = { path: string; size: number; modified: number }
export type MemoryEntry = { author: string | null; timestamp: string | null; text: string }

export type Segment = { kind: 'equal' | 'delete' | 'insert'; text: string }
export type DiffLine = {
  type: 'context' | 'delete' | 'insert'
  old_no: number | null
  new_no: number | null
  text: string
  segments?: Segment[]
}
export type Hunk = {
  old_start: number
  old_count: number
  new_start: number
  new_count: number
  lines: DiffLine[]
}
export type Compare = {
  old: string
  new: string
  old_blocks: number
  new_blocks: number
  stats: { changed: number; added: number; removed: number }
  hunks: Hunk[]
}

export type ChatItem =
  | { kind: 'message'; role: 'user' | 'assistant'; text: string }
  | { kind: 'tool_call'; name: string; args: Record<string, unknown> }
  | { kind: 'tool_result'; name: string; response: Record<string, unknown> }
  | { kind: 'error'; text: string }

type StreamEvent = ChatItem | { kind: 'session'; session_id: string } | { kind: 'done' }

async function failure(response: Response): Promise<Error> {
  const body = await response.json().catch(() => null)
  return new Error(body?.detail ?? `${response.status} ${response.statusText}`)
}

async function getJson<T>(url: string): Promise<T> {
  const response = await fetch(url)
  if (!response.ok) throw await failure(response)
  return response.json() as Promise<T>
}

export const api = {
  status: () => getJson<Status>('/api/status'),
  skills: () => getJson<Skill[]>('/api/skills'),
  memory: (query: string) => getJson<MemoryEntry[]>(`/api/memory?query=${encodeURIComponent(query)}`),
  documents: () => getJson<DocFile[]>('/api/documents'),
  async upload(file: File): Promise<DocFile> {
    const response = await fetch(`/api/documents/${encodeURIComponent(file.name)}`, {
      method: 'PUT',
      body: file,
    })
    if (!response.ok) throw await failure(response)
    return response.json() as Promise<DocFile>
  },
  async compare(oldName: string, newName: string, signal?: AbortSignal): Promise<Compare> {
    const response = await fetch('/api/compare', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ old: oldName, new: newName }),
      signal,
    })
    if (!response.ok) throw await failure(response)
    return response.json() as Promise<Compare>
  },
}

export async function streamAsk(
  body: { old: string; new: string; question: string; session_id: string | null },
  onEvent: (event: StreamEvent) => void,
): Promise<void> {
  const response = await fetch('/api/ask', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!response.ok || !response.body) throw await failure(response)

  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''
  for (;;) {
    const { done, value } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })
    const frames = buffer.split('\n\n')
    buffer = frames.pop() ?? ''
    for (const frame of frames) {
      if (frame.startsWith('data: ')) onEvent(JSON.parse(frame.slice(6)) as StreamEvent)
    }
  }
}

export function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`
}
