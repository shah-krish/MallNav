'use client';
import React, {useEffect, useState} from 'react'
import { fetchStores, Store } from '@/services/api';

function formatHours(hours?: Store['hours']): string{
    if (!hours) return 'Hours not available';
    const firstDay = Object.values(hours)[0];
    if (!firstDay) return 'Hours not available';
    if (firstDay.is_closed) return 'Closed';
    if (firstDay.open && firstDay.close) return `${firstDay.open} - ${firstDay.close}`;
    return 'Hours available upon request';
}

function StoreCard ({store}: {store: Store}){
    return(
        <article className='border border-gray-200 rounded-lg p-4 bg-white shadow-sm'>
            <h2 className='text-lg font-bold text-gray-900'>{store.name}</h2>
            <p className='text-sm text-gray-600'>{store.category}</p>
            <p className='text-xs text-gray-500'>Hours: {formatHours(store.hours)}</p>
            {store.accessible && (
                <p className='mt-3 inline-block w-fit text-xs font-sans font-semibold bg-emerald-600 text-white px-2 py-0.5 rounded'>Accessible Store</p>
            )}
        </article>
    )
}

export default function Page() {
    // stores = actual list of stores. setStores = function to alter stores. <Store[]> tells ts that this variable will contain an array of Stores
    const [stores, setStores] = useState<Store[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // searchName stores the search text. It is initially empty hence ('')
    const[searchName, setSearchName] = useState('');
    // initially all the stores are displayed ('all')
    const [searchCategory, setSearchCategory] = useState('all');
    // initially all the stores are displayed ('false') [accessible only = false]
    const [searchAccessible, setSearchAccessible] = useState(false);

    // fetch stores as soon as the page loads
    // .then() = runs the code after the request succeeds
    // data is the store information returned by backend
    useEffect(() => {
        fetchStores().then((data) => {
            setStores(data);
            setError(null)
        })
        .catch((err) => {
            setError(err.message || 'Something went wrong while fetching the stores.')
        })
        .finally(() => {
            setLoading(false);
        });
        // The last empty array }, []); is the dependency array. It means Fetch the stores when the page first opens, not every time it updates. 
    }, []);

    const filteredStores = stores.filter((store) => 
        store.name.toLowerCase().includes(searchName.toLowerCase()) &&
        (searchCategory === 'all' || store.category === searchCategory) &&
        (!searchAccessible || store.accessible)
    );
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
            
            {/* If loading is true, display loading stores from backend */}
            {loading && <p className='text-gray-500'>Loading stores from backend...</p>}

            {/* If error is true, display Could not load stores and actual error message stored in error variable */}
            {error && (
              <div className='p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg'>
                <p className='font-semibold'>Could not load stores</p>
                <p className='text-sm'>{error}</p>
              </div>
            )}
    
            {/* If no error and not loading but no stores matching the filter */}
            {!loading && !error && filteredStores.length === 0 && (
              <p className='text-gray-500'>No stores found matching your criteria.</p>
            )}

            {/* Else display the relevant stores */}
            {!loading && !error && (
            // grid-cols-1 is mobile default, md is for medium screens, lg is for large screens 
              <section className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4'>
                {filteredStores.map((store) => (
                  <StoreCard key={store.id} store={store} />
                ))}
              </section>
            )}
          </main>
        </div>
      );
}
