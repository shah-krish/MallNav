const BASE_URL = process.env.NEXT_PUBLIC_API_URL;

export interface DayHours{
    open?: string;
    close?:string;
    is_closed: boolean;
}

export interface Store{
    id: string;
    name: string;
    category: string;
    hours?: Record<string, DayHours> | null;
    accessible: boolean;
    zone: string;
    amenities: string[];
    coordinates: [number, number];
}
// Promise means that the result will be available in future. 
// This function will fetch stores from a server and eventually return a list of stores.
export async function fetchStores(): Promise<Store[]> {
    const response = await fetch('${BASE_URL}/stores/')
    if(!response.ok){
        throw new Error('Failed to fetch stores: ${response.statusText}');
    }
    return response.json()
}