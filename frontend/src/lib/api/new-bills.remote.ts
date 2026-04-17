import { query } from '$app/server';
import { BACKEND_HOST, BACKEND_PORT } from '$env/static/private';
import type { BillDetail } from '$lib/types';
import * as v from 'valibot';

const BillsSchema = v.object({
    congress: v.string(),
    type: v.string(),
    offset: v.string(),
    limit: v.string()
});

export const newBills = query(BillsSchema, async (input): Promise<BillDetail[]> => {
    const res = await fetch(
        `http://${BACKEND_HOST}:${BACKEND_PORT}/bills/${input.congress}/${input.type.toLowerCase()}?offset=${input.offset}&limit=${input.limit}`
    );
    const bills: Promise<BillDetail[]> = await res.json();

    return bills;
});
