<script lang="ts">
    import AppSidebar from '$lib/components/app-sidebar.svelte';
    import * as Breadcrumb from '$lib/components/ui/breadcrumb/index.js';
    import { Separator } from '$lib/components/ui/separator/index.js';
    import * as Sidebar from '$lib/components/ui/sidebar/index.js';

    import './layout.css';
    import favicon from '$lib/assets/favicon.svg';
    import { ModeWatcher } from 'mode-watcher';
    import SunIcon from '@lucide/svelte/icons/sun';
    import MoonIcon from '@lucide/svelte/icons/moon';

    import { toggleMode } from 'mode-watcher';
    import Button from '$lib/components/ui/button/button.svelte';

    let { children } = $props();
</script>

<svelte:head><link rel="icon" href={favicon} /></svelte:head>
<ModeWatcher />

<div>
    <Sidebar.Provider>
        <AppSidebar />
        <Sidebar.Inset>
            <header class="flex h-16 shrink-0 items-center gap-2">
                <div class="place-between flex w-full">
                    <div class="flex items-center gap-2 px-4">
                        <Sidebar.Trigger class="-ms-1" />
                        <Separator
                            orientation="vertical"
                            class="me-2 data-[orientation=vertical]:h-4"
                        />
                        <Breadcrumb.Root>
                            <Breadcrumb.List>
                                <Breadcrumb.Item class="hidden md:block">
                                    <Breadcrumb.Link href="##"
                                        >Build Your Application</Breadcrumb.Link
                                    >
                                </Breadcrumb.Item>
                                <Breadcrumb.Separator class="hidden md:block" />
                                <Breadcrumb.Item>
                                    <Breadcrumb.Page>Data Fetching</Breadcrumb.Page>
                                </Breadcrumb.Item>
                            </Breadcrumb.List>
                        </Breadcrumb.Root>
                    </div>
                </div>
                <div class="pr-6">
                    <Button onclick={toggleMode} variant="outline" size="icon">
                        <SunIcon
                            class="h-[1.2rem] w-[1.2rem] scale-100 rotate-0 !transition-all dark:scale-0 dark:-rotate-90"
                        />
                        <MoonIcon
                            class="absolute h-[1.2rem] w-[1.2rem] scale-0 rotate-90 !transition-all dark:scale-100 dark:rotate-0"
                        />
                        <span class="sr-only">Toggle theme</span>
                    </Button>
                </div>
            </header>
            <div class="flex flex-1 flex-col gap-4 p-4">
                <div class="flex min-h-screen flex-1 flex-col rounded-xl md:min-h-min">
                    {@render children()}
                </div>
            </div>
        </Sidebar.Inset>
    </Sidebar.Provider>
</div>
