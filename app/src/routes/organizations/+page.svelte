<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	let organizations = [];
	let providersByOrganization = {};
	let serverLoaded = false;
	let showMoreText = {};

	onMount(async () => {
		const response = await fetch('http://localhost:8888/provider');
		const data = await response.json();
		const providers = data.providers;
		const seenOrganizations = new Set();
		for (const provider of providers) {
			const organization = provider.organization;
			const organizationId = organization.id;
			if (!seenOrganizations.has(organizationId)) {
				organizations.push(organization);
				seenOrganizations.add(organizationId);
				showMoreText[organizationId] = 'Show More';
			}
			if (!providersByOrganization[organizationId]) {
				providersByOrganization[organizationId] = {};
			}
			const specialty = provider.speciality;
			if (!providersByOrganization[organizationId][specialty]) {
				providersByOrganization[organizationId][specialty] = [];
			}
			providersByOrganization[organizationId][specialty].push(provider);
		}
		serverLoaded = true;
	});

	function toggleMoreInfo(id) {
		const moreInfoElement = document.getElementById(id);
		if (moreInfoElement.hidden) {
			moreInfoElement.hidden = false;
			showMoreText[id] = 'Show Less';
		} else {
			moreInfoElement.hidden = true;
			showMoreText[id] = 'Show More';
		}
	}
</script>

<button
	class="route-button profile-button"
	on:click={() => {
		goto('/profile');
	}}>My Profile</button
>
<button
	class="route-button logout-button"
	on:click={() => {
		localStorage.removeItem('ssn');
		localStorage.removeItem('pid');
		goto('/');
	}}>Logout</button
>
<div class="container">
	<h1>Organizations</h1>
	{#if !serverLoaded}
		<div class="loading"><h3><i class="fa fa-spinner fa-spin" /> Loading</h3></div>
	{:else if Object.keys(organizations).length > 0 && serverLoaded}
		{#each organizations as organization}
			<div class="card">
				<h2>{organization.name}</h2>
				<p><strong>Address:</strong> {organization.address}</p>
				<p><strong>City:</strong> {organization.city}</p>
				<p><strong>State:</strong> {organization.state}</p>
				<button on:click={() => toggleMoreInfo(organization.id)}
					>{showMoreText[organization.id]}
				</button>
				<div id={organization.id} class="more-info" hidden>
					<h2>Specialties</h2>
					{#each Object.keys(providersByOrganization[organization.id]) as specialty}
						<div class="specialty">
							<h4>{specialty}</h4>
							<ul>
								{#each providersByOrganization[organization.id][specialty] as provider}
									<li>{provider.name}</li>
								{/each}
							</ul>
						</div>
					{/each}
				</div>
			</div>
		{/each}
	{:else}
		<div class="card">
			<p>No organizations found.</p>
		</div>
	{/if}
</div>

<style>
	.route-button {
		position: absolute;
		top: 20px;
		background-color: rgba(0, 0, 0, 0.7);
		border-radius: 10%;
		color: white;
		padding: 1rem 2rem;
		text-align: center;
		font-size: 1rem;
		cursor: pointer;
	}

	.profile-button {
		right: 10rem;
	}
	.logout-button {
		right: 1rem;
	}
	h2 {
		font-size: large;
		font-weight: bold;
	}
	.container {
		display: flex;
		flex-direction: column;
	}

	.card {
		box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
		transition: 0.3s;
		width: 100%;
		display: inline-block;
		vertical-align: top;
		margin-bottom: 1rem;
		border: solid thin #ccc;
		border-radius: 5px;
		padding: 0.5rem;
	}

	.fa-spinner {
		font-size: 2rem;
	}
	h3 {
		font-size: 2rem;
	}
	.loading {
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.more-info {
		margin-top: 10px;
	}
</style>
