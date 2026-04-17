<script lang="ts">
    import BillDetailCard from '$lib/components/bills/bill-detail-card.svelte';
    import type { PageProps } from './$types';

    let { data }: PageProps = $props();
</script>

<div class="flex h-min w-full justify-center px-4">
    <BillDetailCard {...data.bill} />
</div>
