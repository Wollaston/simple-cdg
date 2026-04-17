<script lang="ts">
    import { Button } from '$lib/components/ui/button';
</script>

<div>
    <h1 class="m-2 p-2 pl-4 text-4xl font-bold">Bills</h1>
    <h1 class="p-4 font-semibold">There are a few features to explore:</h1>
    <ul class="ml-6 pl-6">
        <li>
            <Button class="text-lg" variant="link" href="/bills/search"
                >Semantic Search of Bills</Button
            >
        </li>
        <li>
            <Button class="text-lg" variant="link" href="/bills/view">Viewing Bill Metadata</Button>
        </li>
        <li>
            <Button class="text-lg" variant="link" href="/bills/view"
                >Retrieving and Indexing New Bills</Button
            >
        </li>
    </ul>
</div>
