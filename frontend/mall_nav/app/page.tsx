export default function Home(){
  return(
    <main className="max-w-4xl mx-auto p-8">
      <h1 className="text-4xl font-bold">MallNav: Canadian mall navigator</h1>
      <p>MallNav brings mall navigation and store finding right to your phone, so you can skip the kiosk queue and find your way around with ease!</p>
      <div className="h-64 bg-gray-200 flex items-center justify-center my-8 border-2 border-dashed border-gray-600">
        <span className="font-medium text-gray-700">Screenshot Placeholder</span>
      </div>
      <h2 className="text-2xl font-semibold mb-2">Execution Roadmap</h2>
        <ul className="list-disc pl-6 space-y-1">
          <li>Month 1: Next.js UI & FastAPI foundation</li>
          <li>Month 2: Operational workflows & storage</li>
          <li>Month 3: Search & change-approval states</li>
          <li>Month 4: Async pipelines & observability</li>
        </ul>
    </main>
  )
}