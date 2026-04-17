import { getBillsDetailed } from '$lib/api/detailed-bills.remote';

export async function load() {
    return { bills: await getBillsDetailed() };
}
