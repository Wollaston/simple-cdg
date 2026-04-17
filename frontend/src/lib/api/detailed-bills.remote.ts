import { query } from '$app/server';
import { BACKEND_HOST, BACKEND_PORT } from '$env/static/private';
import type { BillDetail } from '$lib/types';

export const getBillsDetailed = query(async (): Promise<BillDetail[]> => {
    const res = await fetch(`http://${BACKEND_HOST}:${BACKEND_PORT}/bills/list`);
    const bills: Promise<BillDetail[]> = await res.json();

    return bills;
});
