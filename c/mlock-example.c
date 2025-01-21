#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/mman.h>

/* Adapted from
 * https://docs.redhat.com/en/documentation/red_hat_enterprise_linux_for_real_time/7/html/reference_guide/using_mlock_to_avoid_page_io#Using_mlock_to_avoid_page_io
 *
 * Compile with:
 * $ gcc -o mlock-example mlock-example.c
 */

void *
alloc_workbuf(size_t size)
{
	/*
	* alloc memory aligned to a page, to prevent two mlock() in the
	* same page.
	*/
	void *ptr;
	int retval;

	retval = posix_memalign(&ptr, (size_t) sysconf(_SC_PAGESIZE), size);

	/* return NULL on failure */
	if (retval)
		printf("Failed to memalign\n");
		return NULL;

	/* lock this buffer into RAM */
	if (mlock(ptr, size)) {
		printf("Failed to mlock pointer\n");
		free(ptr);
		return NULL;
	}

	return ptr;
}

void
free_workbuf(void *ptr, size_t size)
{
	/* unlock the address range */
	munlock(ptr, size);

	/* free the memory */
	free(ptr);
}

void main(int argc, char **argv)
{
	printf("Peforming mlock memory allocation...\n");
	void *mem = alloc_workbuf(sizeof(int));
	free_workbuf(mem, sizeof(*mem));
	printf("Done.\n");
}
