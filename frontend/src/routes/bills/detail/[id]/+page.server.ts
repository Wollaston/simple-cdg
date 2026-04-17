import { getBillDetail } from '$lib/api/detailed-bill.remote';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params }) => {
    const bill = await getBillDetail({ id: params.id });

    return {
        bill
    };
};
