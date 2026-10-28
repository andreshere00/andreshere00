const LINKS = ['Chat', 'Workspace', 'Skills', 'Memory']

export function SiteFooter({ model }: { model?: string }) {
  return (
    <footer className="module section grid gap-8 md:grid-cols-2">
      <div className="flex flex-col gap-2">
        <span className="eyebrow">Coding agent</span>
        <p className="max-w-[40ch] text-sm">
          Built with Google ADK. Files, memory and code execution stay on this machine; only model
          requests go to OpenRouter.
        </p>
      </div>
      <ul className="flex flex-col gap-3 md:items-end">
        {LINKS.map((label) => (
          <li key={label} className="list-none">
            <a href={`#${label.toLowerCase()}`} className="text-sm text-charcoal hover:text-orange">
              {label}
            </a>
          </li>
        ))}
      </ul>
      <div className="hairline col-span-full flex flex-wrap justify-between gap-4 pt-4 text-xs">
        <span>Model: {model ?? '–'}</span>
        <span>Local-first workspace</span>
      </div>
    </footer>
  )
}
