import { ArrowRight } from 'lucide-react'

export function Hero() {
  return (
    <section id="top" className="flex flex-col">
      <div
        aria-hidden
        className="relative h-[max(200px,calc(32vh-var(--header-height)))] w-full overflow-hidden bg-[#b8481a]"
      >
        <div
          className="absolute -inset-[10%] blur-[60px]"
          style={{
            background: [
              'radial-gradient(circle at 4% 38%, #ffc79d 0 9%, transparent 22%)',
              'radial-gradient(ellipse at 52% 42%, #5a2a1a 0 8%, transparent 24%)',
              'radial-gradient(circle at 48% 86%, #c4501b 0 14%, transparent 34%)',
              'radial-gradient(circle at 96% 70%, #f1a070 0 6%, transparent 18%)',
              'radial-gradient(ellipse at 20% 100%, #3b1608 0 18%, transparent 46%)',
              'linear-gradient(160deg, #e8773a 0%, #d2602a 45%, #8a3412 100%)',
            ].join(','),
          }}
        />
      </div>
      <div className="module section grid grid-cols-12 gap-3 md:gap-3.5">
        <h1 className="heading-xl col-span-12 md:col-span-5">
          See what
          <br />
          changed
        </h1>
        <div className="col-span-12 flex flex-col gap-6 md:col-span-6 md:col-start-7 lg:col-start-6">
          <p className="max-w-[60ch] text-lg md:text-xl">
            Compare two Word documents in a git-style diff, then ask questions about what they
            say. Everything runs on your own machine.
          </p>
          <a href="#compare" className="eyebrow group inline-flex w-fit items-center gap-2 py-3 text-base">
            Compare documents
            <ArrowRight className="size-5 transition-transform group-hover:translate-x-1" />
          </a>
        </div>
      </div>
    </section>
  )
}
