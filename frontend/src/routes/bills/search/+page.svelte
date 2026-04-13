<script lang="ts">
    import { getBills } from '$lib/api/bills.remote';
    import BillCard from '$lib/components/bills/bill-card.svelte';
</script>

<div>
    <h1 class="m-2 p-2">Search Bills</h1>
    <div class="columns-2 gap-4 md:columns-3">
        {#each await getBills({ text: 'This is a test', begin: 0, end: 0 }) as bill}
            <BillCard id={bill.id} text={bill.text} />
        {/each}
    </div>
</div>
