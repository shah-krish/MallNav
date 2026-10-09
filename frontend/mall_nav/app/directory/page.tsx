import React from 'react'

type Store = {
    id: string,
    name: string,
    category: string,
    hours: string,
}

const INITIAL_STORES: Store[] = [
  { id: '1', name: 'Nike Factory Store', category: 'Footwear', hours: '10 AM - 9 PM',},
  { id: '2', name: 'Bass Pro Shops', category: 'Outdoor', hours: '9 AM - 9 PM'},
  { id: '3', name: 'Aroma Espresso Bar', category: 'Dining', hours: '8 AM - 8 PM'},
  { id: '4', name: 'Uniqlo', category: 'Apparel', hours: '10 AM - 9 PM'},
];

function StoreCard ({store}: {store: Store}){
    return(
        <article className='border border-gray-200 rounded-lg p-4 bg-white shadow-sm'>
            <h2 className='text-lg font-bold text-gray-900'>{store.name}</h2>
            <p className='text-sm text-gray-600'>{store.category}</p>
            <p className='text-xs text-gray-500'>Hours: {store.hours}</p>
        </article>
    )
}

export default function page() {
  return (
    <div>
        <main className='max-w-4xl mx-auto p-8 space-y-6'>
            <header>
                <h1 className='text-3xl font-bold'>Mall Directory</h1>
            </header>
            {/* grid-cols-1 is mobile default, md is for medium screens, lg is for large screens */}
            <section className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4'>
                {
                    // (store) is parameter name[on loop1, holds the first object then second then....]
                    // => arrow operator
                    // () instead of {} as no need to return manually if () 
                    // key = mandatory identifier
                    // store = {store} for that iteration stored in store, apply StoreCard function on it
                    INITIAL_STORES.map((store) => (
                     <StoreCard key = {store.id} store = {store}></StoreCard>   
                    ))
                }
            </section>
        </main>
    </div>
  )
}
