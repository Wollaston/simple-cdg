<script lang="ts">
    import { Button } from '$lib/components/ui/button/index.js';
    import * as Card from '$lib/components/ui/card/index.js';
    import { Input } from '$lib/components/ui/input/index.js';
    import { FieldGroup, Field, FieldLabel } from '$lib/components/ui/field/index.js';
    import { enhance } from '$app/forms';
    import type { ActionData } from '../../../routes/auth/login/$types';

    let { form }: { form: ActionData } = $props();
    const id = $props.id();
</script>

<Card.Root class="mx-auto w-full max-w-sm">
    <Card.Header>
        <Card.Title class="text-2xl">Sign Up</Card.Title>
        <Card.Description
            >Enter your name, email, and password below to create your account</Card.Description
        >
    </Card.Header>
    <Card.Content>
        <form method="post" action="?/signUpEmail" use:enhance>
            <FieldGroup>
                <Field>
                    <FieldLabel for="name-{id}">Name</FieldLabel>
                    <Input id="name-{id}" type="text" name="name" required />
                </Field>
                <Field>
                    <FieldLabel for="email-{id}">Email</FieldLabel>
                    <Input
                        id="email-{id}"
                        type="email"
                        name="email"
                        placeholder="me@example.com"
                        required
                    />
                </Field>
                <Field>
                    <FieldLabel for="password-{id}">Password</FieldLabel>
                    <Input id="password-{id}" type="password" name="password" required />
                </Field>
                <Field>
                    <p class="text-red-500">{form?.message ?? ''}</p>
                    <Button type="submit" class="w-full">Sign Up</Button>
                </Field>
            </FieldGroup>
        </form>
    </Card.Content>
</Card.Root>
