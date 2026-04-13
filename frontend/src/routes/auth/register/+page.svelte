<script lang="ts">
    import type { ActionData } from './$types';
    import RegisterForm from '$lib/components/auth/register-form.svelte';

    let { form }: { form: ActionData } = $props();
</script>

<div class="flex h-screen w-full items-center justify-center px-4">
    <RegisterForm {form} />
</div>
