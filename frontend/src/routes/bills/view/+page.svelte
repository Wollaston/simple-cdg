<script lang="ts">
    import BillsTable from '$lib/components/tables/bills-table.svelte';
    import { columns } from '$lib/components/tables/columns';

    let { data } = $props();
</script>

<div>
    <h1 class="m-2 p-2 pl-4 text-4xl font-bold">View Bills</h1>
    <BillsTable data={data.bills} {columns} />
</div>
