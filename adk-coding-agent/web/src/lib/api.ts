export type Status = {
  model: string
  llm_configured: boolean
  sandbox: string
  skills: number
  files: number
  sessions: number
}

export type Skill = { name: string; description: string; source: 'local' | 'vendor' }
export type WorkspaceFile = { path: string; size: number; modified: number }
export type FileContent = { path: string; size: number; text: string | null }
export type MemoryEntry = { author: string | null; timestamp: string | null; text: string }
export type SessionInfo = { id: string; updated: number }

export type ChatItem =
  | { kind: 'message'; role: 'user' | 'assistant'; text: string }
  | { kind: 'tool_call'; name: string; args: Record<string, unknown> }
  | { kind: 'tool_result'; name: string; response: Record<string, unknown> }
  | { kind: 'error'; text: string }

type StreamEvent = ChatItem | { kind: 'session'; session_id: string } | { kind: 'done' }

async function getJson<T>(url: string): Promise<T> {
  const response = await fetch(url)
  if (!response.ok) throw new Error(`${response.status} ${response.statusText}`)
  return response.json() as Promise<T>
}

export const api = {
  status: () => getJson<Status>('/api/status'),
  skills: () => getJson<Skill[]>('/api/skills'),
  files: () => getJson<WorkspaceFile[]>('/api/files'),
  file: (path: string) => getJson<FileContent>(`/api/files/content?path=${encodeURIComponent(path)}`),
  memory: (query: string) => getJson<MemoryEntry[]>(`/api/memory?query=${encodeURIComponent(query)}`),
  sessions: () => getJson<SessionInfo[]>('/api/sessions'),
  history: (id: string) => getJson<ChatItem[]>(`/api/sessions/${encodeURIComponent(id)}`),
}

export async function streamChat(
  sessionId: string | null,
  message: string,
  onEvent: (event: StreamEvent) => void,
  signal?: AbortSignal,
): Promise<void> {
  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId, message }),
    signal,
  })
  if (!response.ok || !response.body) throw new Error(`${response.status} ${response.statusText}`)

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
