import { query } from '$app/server';
import { BACKEND_HOST, BACKEND_PORT } from '$env/static/private';
import type { BillDetail } from '$lib/types';
import * as v from 'valibot';

const BillDetailSchema = v.object({
    id: v.string()
});

export const getBillDetail = query(BillDetailSchema, async (input): Promise<BillDetail> => {
    const res = await fetch(`http://${BACKEND_HOST}:${BACKEND_PORT}/bills/detail`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json'
        },
        body: JSON.stringify({ id: input.id })
    });
    const bill: Promise<BillDetail> = await res.json();

    return bill;
});
