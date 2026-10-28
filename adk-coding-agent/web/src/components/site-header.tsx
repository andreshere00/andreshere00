import { Button } from '@/components/ui/button'

const NAV = [
  { href: '#chat', label: 'Chat' },
  { href: '#workspace', label: 'Workspace' },
  { href: '#skills', label: 'Skills' },
  { href: '#memory', label: 'Memory' },
]

export function SiteHeader() {
  return (
    <header className="fixed inset-x-0 top-0 z-10 h-(--header-height) bg-warm-gray-01">
      <div className="module flex h-full items-center justify-between">
        <a href="#top" className="flex items-center gap-3 text-navy" aria-label="Coding agent">
          <span className="grid size-8 place-items-center bg-navy font-mono text-sm text-white">
            <span>
              &gt;<span className="text-orange">_</span>
            </span>
          </span>
          <span className="eyebrow hidden sm:inline">Coding agent</span>
        </a>
        <nav className="flex items-center">
          {NAV.map((item) => (
            <Button
              key={item.href}
              variant="ghost"
              className="px-2 text-xs md:px-5 md:text-sm"
              nativeButton={false}
              render={<a href={item.href} />}
            >
              {item.label}
            </Button>
          ))}
        </nav>
      </div>
    </header>
  )
}
