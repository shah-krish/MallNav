'use client';
import React, {useState} from 'react'

type Store = {
    id: string,
    name: string,
    category: string,
    hours: string,
    accessible: boolean
}

const INITIAL_STORES: Store[] = [
  { id: '1', name: 'Nike Factory Store', category: 'Footwear', hours: '10 AM - 9 PM', accessible: true},
  { id: '2', name: 'Bass Pro Shops', category: 'Outdoor', hours: '9 AM - 9 PM', accessible: true},
  { id: '3', name: 'Aroma Espresso Bar', category: 'Dining', hours: '8 AM - 8 PM', accessible: true},
  { id: '4', name: 'Uniqlo', category: 'Apparel', hours: '10 AM - 9 PM', accessible: false},
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

export default function Page() {
    const [searchName, setSearchName] = useState("")
    const [searchCategory, setSearchCategory] = useState("all")
    const [searchAccessible, setSearchAccessible] = useState(false)
    const filteredStores = INITIAL_STORES.filter((store)=>
        store.name.toLowerCase().includes(searchName.toLowerCase()) 
        && (searchCategory === "all" || store.category === searchCategory) 
        && (!searchAccessible || store.accessible)
    )
  return (
    <div>
        <main className='max-w-4xl mx-auto p-8 space-y-6'>
            <header>
                <h1 className='text-3xl font-bold'>Mall Directory</h1>
            </header>
            <section className='flex gap-2 items-center'>
                <input className='border border-gray-600 rounded-xl pl-3 p-1' 
                                placeholder='Search MallNav' 
                                type="text" 
                                value = {searchName}
                                // when input value changes, event e is triggered which sets the search value
                                onChange = {(e) => setSearchName(e.target.value)}></input>
                <select id = "category" value = {searchCategory} onChange={(e) => setSearchCategory(e.target.value)}>
                            <option value="all">All categories</option>
                            <option value="Footwear">Footwear</option>
                            <option value="Dining">Dining</option>
                            <option value="Apparel">Apparel</option>
                            <option value ="Outdoor">Outdoor</option>
                </select>
                <label className='flex items-center gap-1'>
                    Accessible?
                    <input type = "checkbox" checked = {searchAccessible} onChange={(e) => setSearchAccessible(e.target.checked)}></input>    
                </label>
            </section>
            {/* grid-cols-1 is mobile default, md is for medium screens, lg is for large screens */}
            <section className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4'>
                {
                    // (store) is parameter name[on loop1, holds the first object then second then....]
                    // => arrow operator
                    // () instead of {} as no need to return manually if () 
                    // key = mandatory identifier
                    // store = {store} for that iteration stored in store, apply StoreCard function on it
                    filteredStores.map((store) => (
                     <StoreCard key = {store.id} store = {store}></StoreCard>   
                    ))
                }
            </section>
        </main>
    </div>
  )
}
